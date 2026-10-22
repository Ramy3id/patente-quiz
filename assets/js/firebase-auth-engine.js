/**
 * =======================================================================
 * Patente B Pro - Cloud Authentication & Firestore Sync Engine (2026)
 * =======================================================================
 * @author Eng. Ramy Eid Saad Fahmy & Architecture Team
 * @description
 * - المحرك السحابي المتكامل للحسابات والمزامنة الفورية عبر Google Firebase.
 * - التسجيل الكامل بالبيانات: (الاسم، اللقب، البريد، كلمة المرور، الهاتف، تاريخ الميلاد، النوع).
 * - تسجيل الدخول بالبريد الإلكتروني أو حساب Google بنقرة واحدة.
 * - مزامنة إنجاز الـ 25 باباً، بنك الأخطاء، وسجل الامتحانات تلقائياً عبر الأجهزة.
 * - تصميم Apple HIG كامل التجاوب مع الثيم الليلي والنهاري (Light/Dark Mode).
 */

(function () {
  'use strict';

  // 1. مفاتيح إعدادات مشروع Firebase الرسمي
  const FIREBASE_CONFIG = {
    apiKey: "AIzaSyBVnl-gy7sGsdG5M6dTmhYU7ZI5VUblH7s",
    authDomain: "patente-b-pro.firebaseapp.com",
    projectId: "patente-b-pro",
    storageBucket: "patente-b-pro.firebasestorage.app",
    messagingSenderId: "170993396640",
    appId: "1:170993396640:web:14024c306960017f9d52c5",
    measurementId: "G-0XKH713DCV"
  };

  // حالة النظام والمستخدم الحالي
  let authApp = null;
  let authInstance = null;
  let firestoreInstance = null;
  let currentUser = null;
  let userProfile = null;
  let isSyncing = false;
  let lastSyncTime = null;
  let isRegistrationInProgress = false;
  let lastUnverifiedCredentials = null;
  let lastRegisteredCredentials = null;

  // دالة مساعدة لحماية النصوص من ثغرات الحقن (XSS Sanitizer)
  function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
  window.escapeHtml = window.escapeHtml || escapeHtml;

  // 2. تحميل مكتبات Firebase SDK ديناميكياً بشكل متسلسل آمن
  function loadSingleScript(src) {
    return new Promise((resolve, reject) => {
      if (document.querySelector(`script[src="${src}"]`)) return resolve();
      const script = document.createElement('script');
      script.src = src;
      script.onload = () => resolve();
      script.onerror = (err) => {
        console.warn('تعذر تحميل السكربت:', src, err);
        reject(err);
      };
      document.head.appendChild(script);
    });
  }

  async function loadFirebaseSDKs() {
    if (window.firebase && window.firebase.auth && window.firebase.firestore) {
      return window.firebase;
    }

    // 1. يجب تحميل app-compat أولاً لتعريف window.firebase
    await loadSingleScript('https://www.gstatic.com/firebasejs/10.14.1/firebase-app-compat.js');

    // 2. تحميل auth و firestore معاً
    await Promise.all([
      loadSingleScript('https://www.gstatic.com/firebasejs/10.14.1/firebase-auth-compat.js'),
      loadSingleScript('https://www.gstatic.com/firebasejs/10.14.1/firebase-firestore-compat.js')
    ]);

    return window.firebase;
  }

  // 3. تهيئة النظام السحابي
  async function initFirebase() {
    try {
      const fb = await loadFirebaseSDKs();
      if (!fb.apps.length) {
        authApp = fb.initializeApp(FIREBASE_CONFIG);
      } else {
        authApp = fb.app();
      }

      authInstance = fb.auth();
      // ضبط لغة رسائل التحقق واستعادة كلمة المرور الرسمية إلى العربية
      authInstance.languageCode = 'ar';
      firestoreInstance = fb.firestore();

      // تفعيل الكاش الداخلي بدون إنترنت
      try {
        firestoreInstance.enablePersistence({ synchronizeTabs: true }).catch(() => {});
      } catch (_) {}

      // الاستماع لتغير حالة الدخول
      authInstance.onAuthStateChanged(handleAuthStateChange);

      // فحص نتيجة إعادة التوجيه في حال تم الدخول عبر signInWithRedirect (لتفادي حظر النوافذ المنبثقة)
      try {
        await authInstance.getRedirectResult();
      } catch (redirectErr) {
        console.warn('Google redirect result notice:', redirectErr);
      }

      return true;
    } catch (err) {
      console.warn('PatenteAuth: يعمل التطبيق في الوضع المحلي (Offline Mode)');
      updateAuthUiLoggedOut();
    window.dispatchEvent(new CustomEvent('patente:auth-changed', { detail: { loggedIn: false } }));
      return false;
    }
  }

  // 4. معالجة تغير حالة المصادقة (Auth State Change)
  async function handleAuthStateChange(user) {
    if (isRegistrationInProgress) {
      // أثناء التسجيل، تتولى دالة registerAccount إدارة الحالة
      return;
    }

    if (user) {
      const isGoogle = user.providerData && user.providerData.some(p => p.providerId === 'google.com');
      // إذا كان الحساب مسجلاً بالبريد وكلمة المرور ولكنه غير مفعل بعد، لا يُسمح له بالدخول إطلاقاً
      if (!isGoogle && !user.emailVerified) {
        currentUser = null;
        userProfile = null;
        try {
          localStorage.removeItem('patente_user_profile');
        } catch (_) {}
        try {
          await authInstance.signOut();
        } catch (_) {}
        updateAuthUiLoggedOut();
        window.dispatchEvent(new CustomEvent('patente:auth-changed', { detail: { loggedIn: false } }));
        return;
      }
    }

    currentUser = user;
    if (user) {
      try {
        // جلب بيانات ملف الطالب من Firestore
        const docRef = firestoreInstance.collection('users').doc(user.uid);
        const docSnap = await docRef.get();
        if (docSnap.exists) {
          userProfile = docSnap.data();
          try {
            localStorage.setItem('patente_user_profile', JSON.stringify(userProfile));
          } catch (_) {}
        } else {
          // محاولة استرجاع البيانات المخزنة محلياً إذا كانت متوفرة
          let cachedProfile = null;
          try {
            const raw = localStorage.getItem('patente_user_profile');
            if (raw) cachedProfile = JSON.parse(raw);
          } catch (_) {}

          if (cachedProfile && cachedProfile.uid === user.uid) {
            userProfile = cachedProfile;
            await docRef.set(userProfile, { merge: true });
          } else {
            // ملف مبدئي لحسابات Google الجديدة
            const nameParts = (user.displayName || 'طالب جديد').split(' ');
            userProfile = {
              uid: user.uid,
              firstName: nameParts[0] || 'طالب',
              lastName: nameParts.slice(1).join(' ') || '',
              fullName: user.displayName || 'طالب جديد',
              email: user.email || '',
              phone: user.phoneNumber || '',
              birthDate: '',
              gender: 'unspecified',
              emailVerified: true,
              createdAt: window.firebase.firestore.FieldValue.serverTimestamp(),
              platform: 'Patente B Pro 2026'
            };
            await docRef.set(userProfile, { merge: true });
          }
          try {
            localStorage.setItem('patente_user_profile', JSON.stringify(userProfile));
          } catch (_) {}
        }

        updateAuthUiLoggedIn(userProfile);
        window.dispatchEvent(new CustomEvent('patente:auth-changed', { detail: { loggedIn: true, user: userProfile } }));

        // مزامنة تلقائية هادئة مع السحابة عند الدخول
        syncBidirectional(user.uid);
      } catch (err) {
        console.error('Error fetching user profile:', err);
        let cachedProfile = null;
        try {
          const raw = localStorage.getItem('patente_user_profile');
          if (raw) cachedProfile = JSON.parse(raw);
        } catch (_) {}

        userProfile = cachedProfile || {
          uid: user.uid,
          firstName: user.displayName ? user.displayName.split(' ')[0] : 'طالب',
          fullName: user.displayName || 'طالب',
          email: user.email || ''
        };
        updateAuthUiLoggedIn(userProfile);
      }
    } else {
      userProfile = null;
      try {
        localStorage.removeItem('patente_user_profile');
      } catch (_) {}
      updateAuthUiLoggedOut();
    }
  }

  // 5. تسجيل حساب جديد مع التحقق الإلزامي من البريد (Register with Email Verification)
  async function registerAccount({ firstName, lastName, email, password, phone, birthDate, gender }) {
    if (!authInstance) throw new Error('خدمة السحابة غير مهيأة بعد');
    if (!firstName || !firstName.trim() || !lastName || !lastName.trim()) {
      throw new Error('يرجى ملء الاسم الأول واللقب');
    }
    if (!email || !password) {
      throw new Error('يرجى ملء البريد الإلكتروني وكلمة المرور');
    }
    
    // فحص قوة كلمة المرور
    const specialCharRegex = /[^a-zA-Z0-9\s]/;
    if (password.length < 6 || !specialCharRegex.test(password)) {
      throw new Error('كلمة المرور يجب أن تتكون من 6 خانات على الأقل وتتضمن رمزاً خاصاً واحداً على الأقل (مثل: @, #, $, %, !, -, *, +, §)');
    }

    // فحص صيغة البريد الإلكتروني
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.trim())) {
      throw new Error('يرجى إدخال بريد إلكتروني صالح (مثال: name@example.com)');
    }

    // فحص رقم الهاتف بدقة (بين 7 و15 رقماً بعد استبعاد المسافات والرموز)
    const phoneDigits = (phone || '').replace(/\D/g, '');
    if (phoneDigits.length < 7 || phoneDigits.length > 15) {
      throw new Error('يرجى إدخال رقم هاتف صحيح مكوّن من 7 إلى 15 رقماً.');
    }

    isRegistrationInProgress = true;
    let createdUser = null;
    let emailSentSuccess = false;

    try {
      // 1. إنشاء الحساب في Firebase Auth
      const cred = await authInstance.createUserWithEmailAndPassword(email.trim(), password);
      createdUser = cred.user;

      // 2. تحديث الاسم المعروض في Firebase Auth
      const fullName = `${firstName.trim()} ${lastName.trim()}`.trim();
      try {
        await createdUser.updateProfile({ displayName: fullName });
      } catch (_) {}

      // 3. حفظ تفاصيل الملف الشخصي الكاملة في Firestore كحساب بانتظار التفعيل
      const profileData = {
        uid: createdUser.uid,
        firstName: firstName.trim(),
        lastName: lastName.trim(),
        fullName: fullName,
        email: email.trim().toLowerCase(),
        phone: (phone || '').trim(),
        birthDate: birthDate || '',
        gender: gender || 'unspecified',
        emailVerified: false,
        createdAt: window.firebase.firestore.FieldValue.serverTimestamp(),
        lastLoginAt: window.firebase.firestore.FieldValue.serverTimestamp(),
        platform: 'Patente B Pro 2026'
      };

      try {
        await firestoreInstance.collection('users').doc(createdUser.uid).set(profileData);
      } catch (err) {
        console.warn('Firestore profile save notice:', err);
      }

      // 4. إرسال رابط تأكيد وتفعيل الحساب إلى البريد الإلكتروني
      try {
        await createdUser.sendEmailVerification();
        emailSentSuccess = true;
      } catch (sendErr) {
        console.warn('sendEmailVerification notice:', sendErr);
      }

      return {
        success: true,
        email: profileData.email,
        fullName: fullName,
        password: password,
        emailSent: emailSentSuccess
      };
    } finally {
      // 5. طرد وتسجيل خروج المستخدم فوراً وبشكل قاطع، سواء نجح إرسال الإيميل أم حدث خطأ
      isRegistrationInProgress = false;
      currentUser = null;
      userProfile = null;
      try {
        localStorage.removeItem('patente_user_profile');
      } catch (_) {}
      try {
        await authInstance.signOut();
      } catch (_) {}
      updateAuthUiLoggedOut();
      window.dispatchEvent(new CustomEvent('patente:auth-changed', { detail: { loggedIn: false } }));
    }
  }

  // 6. تسجيل الدخول مع فحص تفعيل البريد الإلكتروني
  async function loginAccount(email, password) {
    if (!authInstance) throw new Error('خدمة السحابة غير مهيأة بعد');
    if (!email || !password) throw new Error('يرجى إدخال البريد الإلكتروني وكلمة المرور');

    const cred = await authInstance.signInWithEmailAndPassword(email.trim(), password);
    const user = cred.user;

    // فحص هل البريد مفعل بالرابط
    if (!user.emailVerified) {
      // الحساب لم يتم تفعيله بعد: نحتفظ ببيانات مؤقتة لزر إعادة الإرسال الفوري
      lastUnverifiedCredentials = { email: email.trim(), password: password };

      await authInstance.signOut();
      currentUser = null;
      userProfile = null;
      try {
        localStorage.removeItem('patente_user_profile');
      } catch (_) {}
      updateAuthUiLoggedOut();

      const err = new Error('EMAIL_NOT_VERIFIED');
      err.code = 'auth/email-not-verified';
      err.email = email.trim();
      throw err;
    }

    // الحساب مفعل بنجاح! مسح أي مؤقتات
    lastUnverifiedCredentials = null;

    // تحديث تاريخ آخر دخول وتحديث حالة التفعيل في Firestore
    try {
      await firestoreInstance.collection('users').doc(user.uid).update({
        lastLoginAt: window.firebase.firestore.FieldValue.serverTimestamp(),
        emailVerified: true
      });
    } catch (_) {}

    return user;
  }

  // 6.1 إعادة إرسال رابط تفعيل البريد (Resend Verification Email)
  async function resendVerificationEmail(email, password) {
    if (!authInstance) throw new Error('خدمة السحابة غير مهيأة بعد');
    const targetEmail = (email || (lastUnverifiedCredentials && lastUnverifiedCredentials.email) || (lastRegisteredCredentials && lastRegisteredCredentials.email) || '').trim();
    const targetPass = password || (lastUnverifiedCredentials && lastUnverifiedCredentials.password) || (lastRegisteredCredentials && lastRegisteredCredentials.password);

    if (!targetEmail || !targetPass) {
      throw new Error('يرجى كتابة البريد وكلمة المرور لإعادة إرسال رابط التفعيل.');
    }

    const cred = await authInstance.signInWithEmailAndPassword(targetEmail, targetPass);
    if (cred.user.emailVerified) {
      await authInstance.signOut();
      return { alreadyVerified: true, email: targetEmail };
    }

    await cred.user.sendEmailVerification();
    await authInstance.signOut();
    return { sent: true, email: targetEmail };
  }

  // 7. الدخول عبر Google مع دعم النوافذ المنبثقة وإعادة التوجيه التلقائية (Popup + Redirect Fallback)
  async function loginWithGoogle() {
    if (!authInstance) throw new Error('خدمة السحابة غير مهيأة بعد');
    const provider = new window.firebase.auth.GoogleAuthProvider();
    provider.setCustomParameters({ prompt: 'select_account' });
    try {
      const res = await authInstance.signInWithPopup(provider);
      return res.user;
    } catch (err) {
      // إذا قام المتصفح بحظر النوافذ المنبثقة (popup-blocked في الموبايل أو Safari)، نلجأ لإعادة التوجيه المباشرة
      if (err.code === 'auth/popup-blocked' || err.code === 'auth/cancelled-popup-request') {
        console.warn('Google Auth popup was blocked, falling back to signInWithRedirect:', err);
        await authInstance.signInWithRedirect(provider);
        return null;
      }
      throw err;
    }
  }

  // تفريغ كافة حقول النماذج ومسح أي بيانات مؤقتة (Sanitize & Reset Auth Forms)
  function clearAuthForms() {
    try {
      const loginForm = document.getElementById('authLoginForm');
      if (loginForm && typeof loginForm.reset === 'function') loginForm.reset();

      const regForm = document.getElementById('authRegisterForm');
      if (regForm && typeof regForm.reset === 'function') regForm.reset();

      const inputIds = [
        'loginEmail', 'loginPassword',
        'regFirstName', 'regLastName', 'regEmail', 'regPassword',
        'regPhone', 'regBirthDate'
      ];
      inputIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          el.value = '';
          el.defaultValue = '';
        }
      });

      const genderSelect = document.getElementById('regGender');
      if (genderSelect) genderSelect.value = 'male';

      const phoneCodeSelect = document.getElementById('regPhoneCountryCode');
      if (phoneCodeSelect) phoneCodeSelect.value = '+39';

      lastUnverifiedCredentials = null;
      lastRegisteredCredentials = null;

      const alertBox = document.getElementById('authAlertMsg');
      if (alertBox) {
        alertBox.textContent = '';
        alertBox.className = 'auth-alert-msg';
      }
    } catch (e) {
      console.warn('clearAuthForms notice:', e);
    }
  }

  // 8. تسجيل الخروج (Logout)
  async function logoutAccount() {
    if (!authInstance) return;
    await authInstance.signOut();
    userProfile = null;
    currentUser = null;
    try {
      localStorage.removeItem('patente_user_profile');
    } catch (_) {}
    clearAuthForms();
    updateAuthUiLoggedOut();
  }

  // 8.1 حذف الحساب نهائياً من السحابة والواجهة (Permanent Account Deletion)
  async function deleteCurrentAccount() {
    if (!currentUser) return;
    const uid = currentUser.uid;

    // 1. مسح وثائق المستخدم من Firestore
    try {
      if (firestoreInstance) {
        await firestoreInstance.collection('users').doc(uid).collection('userData').doc('progress').delete();
        await firestoreInstance.collection('users').doc(uid).delete();
      }
    } catch (e) {
      console.warn('Firestore deletion notice:', e);
    }

    // 2. تنظيف التخزين المحلي
    try {
      localStorage.removeItem('patente_user_profile');
    } catch (_) {}

    // 3. حذف الحساب من Firebase Auth
    await currentUser.delete();

    // 4. تحديث حالة الواجهة وتفريغ الحقول بالكامل كـ زائر جديد
    currentUser = null;
    userProfile = null;
    clearAuthForms();
    updateAuthUiLoggedOut();
  }

  // 9. استرجاع كلمة المرور
  async function resetPassword(email) {
    if (!authInstance) throw new Error('خدمة السحابة غير مهيأة');
    await authInstance.sendPasswordResetEmail(email.trim());
  }

  // 10. تجميع التقدم المحلي من المتصفح (Local Data Collector)
  function collectLocalProgress() {
    const chaptersData = {};
    for (let ch = 1; ch <= 25; ch++) {
      try {
        const raw = localStorage.getItem('patente_progress_cap_' + ch);
        if (raw) chaptersData[ch] = JSON.parse(raw);
      } catch (_) {}
    }

    let examHistory = [];
    try {
      const rawHist = localStorage.getItem('patente_exam_history');
      if (rawHist) examHistory = JSON.parse(rawHist);
    } catch (_) {}

    let srsVault = {};
    try {
      const rawSrs = localStorage.getItem('patente_b_pro_srs_vault');
      if (rawSrs) srsVault = JSON.parse(rawSrs);
    } catch (_) {}

    return {
      chapters: chaptersData,
      examHistory,
      srsVault,
      theme: localStorage.getItem('patente_app_theme') || 'dark',
      savedAt: Date.now()
    };
  }

  // 11. رفع التقدم المحلي إلى Firestore
  async function uploadLocalProgressToCloud(uid) {
    if (!firestoreInstance || !uid) return;
    isSyncing = true;
    updateSyncIndicator(true);

    try {
      const localData = collectLocalProgress();
      const progressDocRef = firestoreInstance.collection('users').doc(uid).collection('userData').doc('progress');
      
      await progressDocRef.set({
        ...localData,
        updatedAt: window.firebase.firestore.FieldValue.serverTimestamp()
      }, { merge: true });

      lastSyncTime = new Date();
      updateSyncStatusText(`تمت المزامنة سحابياً: ${lastSyncTime.toLocaleTimeString('ar-EG', { hour: '2-digit', minute: '2-digit' })} 🟢`);
    } catch (err) {
      console.error('Error uploading progress to cloud:', err);
      updateSyncStatusText('تعذرت المزامنة السحابية حالياً ⚠️');
    } finally {
      isSyncing = false;
      updateSyncIndicator(false);
    }
  }

  // 12. جلب التقدم السحابي وتطبيقه محلياً (Cloud to Local Pull)
  async function pullCloudProgressToLocal(uid) {
    if (!firestoreInstance || !uid) return;
    isSyncing = true;
    updateSyncIndicator(true);

    try {
      const docRef = firestoreInstance.collection('users').doc(uid).collection('userData').doc('progress');
      const snap = await docRef.get();

      if (snap.exists) {
        const cloudData = snap.data();

        // دمج الأبواب الـ 25
        if (cloudData.chapters) {
          Object.keys(cloudData.chapters).forEach(ch => {
            const capData = cloudData.chapters[ch];
            if (capData) {
              localStorage.setItem('patente_progress_cap_' + ch, JSON.stringify(capData));
            }
          });
        }

        // دمج سجل الامتحانات
        if (Array.isArray(cloudData.examHistory) && cloudData.examHistory.length > 0) {
          localStorage.setItem('patente_exam_history', JSON.stringify(cloudData.examHistory));
        }

        // دمج بنك الأخطاء
        if (cloudData.srsVault && Object.keys(cloudData.srsVault).length > 0) {
          localStorage.setItem('patente_b_pro_srs_vault', JSON.stringify(cloudData.srsVault));
        }

        // تحديث شارات الهيدر واللوحة الحالية
        if (typeof window.updatePortalProgress === 'function') {
          window.updatePortalProgress();
        }

        window.dispatchEvent(new CustomEvent('patente:cloud-synced', { detail: cloudData }));

        lastSyncTime = new Date();
        updateSyncStatusText(`تمت المزامنة سحابياً: ${lastSyncTime.toLocaleTimeString('ar-EG', { hour: '2-digit', minute: '2-digit' })} 🟢`);
      }
    } catch (err) {
      console.error('Error pulling cloud progress:', err);
    } finally {
      isSyncing = false;
      updateSyncIndicator(false);
    }
  }

  // 13. المزامنة الذكية ثنائية الاتجاه (Bidirectional Sync)
  async function syncBidirectional(uid) {
    if (!firestoreInstance || !uid) return;
    try {
      const docRef = firestoreInstance.collection('users').doc(uid).collection('userData').doc('progress');
      const snap = await docRef.get();

      if (!snap.exists) {
        // لا يوجد بيانات سحابية سابقة: ارفع البيانات المحلية فوراً
        await uploadLocalProgressToCloud(uid);
      } else {
        const cloudData = snap.data();
        const localData = collectLocalProgress();

        // مقارنة التحديث الأحدث أو الدمج
        const cloudTime = cloudData.savedAt || 0;
        const localTime = localData.savedAt || 0;

        if (cloudTime > localTime) {
          await pullCloudProgressToLocal(uid);
        } else {
          await uploadLocalProgressToCloud(uid);
        }
      }
    } catch (e) {
      console.warn('Sync bidirectional warning:', e);
    }
  }

  // =========================================================
  // 14. واجهة المستخدم والتصميم (UI & Apple HIG Modal Suite)
  // =========================================================

  function injectAuthStyles() {
    if (document.getElementById('patenteAuthStyles')) return;
    const style = document.createElement('style');
    style.id = 'patenteAuthStyles';
    style.textContent = `
      /* زر الحساب في الهيدر */
      .nav-auth-pill {
        height: 36px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0 12px;
        border-radius: 9px;
        font-family: inherit;
        font-size: 0.8rem;
        font-weight: 700;
        cursor: pointer;
        border: 1px solid rgba(56, 189, 248, 0.28);
        background: rgba(56, 189, 248, 0.08);
        color: #38BDF8;
        transition: all 0.2s ease;
        position: relative;
        white-space: nowrap;
        outline: none;
        text-decoration: none;
      }
      .nav-auth-pill:hover {
        background: rgba(56, 189, 248, 0.18);
        border-color: rgba(56, 189, 248, 0.5);
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(56, 189, 248, 0.2);
      }
      html.light .nav-auth-pill {
        background: rgba(2, 132, 199, 0.06);
        border-color: rgba(2, 132, 199, 0.25);
        color: #0284C7;
      }
      html.light .nav-auth-pill:hover {
        background: rgba(2, 132, 199, 0.12);
        border-color: rgba(2, 132, 199, 0.45);
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.15);
      }
      .nav-auth-pill.logged-in {
        background: rgba(16, 185, 129, 0.1);
        border-color: rgba(16, 185, 129, 0.35);
        color: #34D399;
      }
      html.light .nav-auth-pill.logged-in {
        background: rgba(5, 150, 105, 0.08);
        border-color: rgba(5, 150, 105, 0.3);
        color: #059669;
      }
      .auth-online-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 8px #10B981;
        display: inline-block;
      }
      .auth-online-dot.syncing {
        background: #F59E0B;
        box-shadow: 0 0 8px #F59E0B;
        animation: authPulse 0.8s infinite alternate;
      }
      @keyframes authPulse {
        from { opacity: 0.4; transform: scale(0.85); }
        to { opacity: 1; transform: scale(1.2); }
      }

      /* نافذة المصادقة المنبثقة الفاخرة - Apple HIG Motion (تناسق كامل بدون سكرول على الديسكتوب) */
      .auth-modal-backdrop {
        position: fixed;
        inset: 0;
        background: rgba(15, 23, 42, 0.78);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        z-index: 100000;
        display: flex;
        align-items: center; /* توسيط عمودي مثالي */
        justify-content: center;
        padding: 16px;
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        overflow: hidden; /* منع السكرول على الديسكتوب */
        transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1),
                    visibility 0.3s ease,
                    backdrop-filter 0.3s ease;
      }
      .auth-modal-backdrop.open {
        opacity: 1;
        visibility: visible;
        pointer-events: auto;
      }
      .auth-modal-card {
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 24px;
        width: 100%;
        max-width: 530px;
        padding: 22px 24px 20px;
        box-shadow: 0 25px 60px -12px rgba(0, 0, 0, 0.75), 0 0 0 1px rgba(255, 255, 255, 0.06);
        transform: scale(0.94) translateY(18px);
        opacity: 0;
        transition: transform 0.34s cubic-bezier(0.32, 0.72, 0, 1),
                    opacity 0.28s cubic-bezier(0.16, 1, 0.3, 1);
        color: #F8FAFC;
        position: relative;
        direction: rtl;
        text-align: right;
        overflow: hidden; /* إخفاء أي شريط تمرير على الديسكتوب */
        scrollbar-width: none;
        box-sizing: border-box;
      }
      .auth-modal-card::-webkit-scrollbar {
        display: none;
        width: 0;
        height: 0;
      }
      html.light .auth-modal-card {
        background: #FFFFFF;
        border-color: rgba(15, 23, 42, 0.12);
        color: #0F172A;
        box-shadow: 0 25px 60px -12px rgba(15, 23, 42, 0.18), 0 0 0 1px rgba(15, 23, 42, 0.05);
      }
      .auth-modal-backdrop.open .auth-modal-card {
        transform: scale(1) translateY(0);
        opacity: 1;
      }

      .auth-close-btn {
        position: absolute;
        top: 16px;
        left: 16px;
        background: rgba(255, 255, 255, 0.08);
        border: none;
        color: #94A3B8;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.95rem;
        transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1),
                    background-color 0.2s ease,
                    color 0.2s ease;
      }
      html.light .auth-close-btn { background: #F1F5F9; color: #475569; }
      .auth-close-btn:hover {
        background: rgba(239, 68, 68, 0.18);
        color: #EF4444;
        transform: scale(1.1) rotate(90deg);
      }
      .auth-close-btn:active {
        transform: scale(0.92);
      }

      /* تبويبات التبديل دخول / تسجيل */
      .auth-tabs-nav {
        display: flex;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 3px;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
      }
      html.light .auth-tabs-nav { background: #F1F5F9; border-color: rgba(15, 23, 42, 0.08); }
      .auth-tab-btn {
        flex: 1;
        padding: 7px 10px;
        border: none;
        background: transparent;
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 700;
        cursor: pointer;
        border-radius: 9px;
        transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
        font-family: inherit;
        position: relative;
      }
      html.light .auth-tab-btn { color: #64748B; }
      .auth-tab-btn:active {
        transform: scale(0.97);
      }
      .auth-tab-btn.active {
        background: #38BDF8;
        color: #0F172A;
        box-shadow: 0 2px 8px rgba(56, 189, 248, 0.35);
      }
      html.light .auth-tab-btn.active {
        background: #0284C7;
        color: #FFFFFF;
      }

      /* حركة النماذج الانسيابية */
      .auth-form-animated {
        animation: authFormSlideIn 0.28s cubic-bezier(0.16, 1, 0.3, 1) both;
        will-change: transform, opacity;
      }
      @keyframes authFormSlideIn {
        from {
          opacity: 0;
          transform: translateY(8px) scale(0.99);
        }
        to {
          opacity: 1;
          transform: translateY(0) scale(1);
        }
      }

      /* حقول الإدخال */
      .auth-field-group {
        margin-bottom: 9px;
      }
      .auth-label {
        display: block;
        font-size: 0.77rem;
        font-weight: 700;
        margin-bottom: 3px;
        color: #94A3B8;
      }
      html.light .auth-label { color: #475569; }
      .auth-input, .auth-select {
        width: 100%;
        height: 38px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #FFF;
        padding: 0 11px;
        font-family: inherit;
        font-size: 0.86rem;
        outline: none;
        transition: border-color 0.2s cubic-bezier(0.16, 1, 0.3, 1),
                    background-color 0.2s ease,
                    box-shadow 0.2s cubic-bezier(0.16, 1, 0.3, 1),
                    transform 0.15s ease;
        box-sizing: border-box;
      }
      html.light .auth-input, html.light .auth-select {
        background: #F8FAFC;
        border-color: rgba(15, 23, 42, 0.15);
        color: #0F172A;
      }
      .auth-input:focus, .auth-select:focus {
        border-color: #38BDF8;
        background: rgba(56, 189, 248, 0.05);
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.18);
        transform: translateY(-1px);
      }
      .auth-row-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
      }

      /* زر الإجراء الأساسي */
      .auth-submit-btn {
        width: 100%;
        height: 42px;
        border-radius: 11px;
        background: #10B981;
        color: #FFFFFF;
        border: none;
        font-size: 0.92rem;
        font-weight: 800;
        cursor: pointer;
        transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1),
                    box-shadow 0.22s cubic-bezier(0.16, 1, 0.3, 1),
                    background-color 0.2s ease;
        font-family: inherit;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        margin-top: 10px;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
        will-change: transform;
      }
      .auth-submit-btn:hover {
        background: #059669;
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.4);
      }
      .auth-submit-btn:active {
        transform: translateY(1px) scale(0.985);
      }
      .auth-submit-btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
      }

      /* زر الدخول بجوجل */
      .auth-google-btn {
        width: 100%;
        height: 38px;
        border-radius: 11px;
        background: #FFFFFF;
        color: #0F172A;
        border: 1px solid rgba(15, 23, 42, 0.15);
        font-size: 0.85rem;
        font-weight: 700;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 9px;
        margin-top: 6px;
        font-family: inherit;
        transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1),
                    box-shadow 0.22s cubic-bezier(0.16, 1, 0.3, 1),
                    background-color 0.2s ease;
        will-change: transform;
      }
      .auth-google-btn:hover {
        background: #F8FAFC;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }
      .auth-google-btn:active {
        transform: translateY(1px) scale(0.985);
      }

      /* تنبيهات الأخطاء والنجاح */
      .auth-alert-msg {
        padding: 9px 12px;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 10px;
        display: none;
      }
      .auth-alert-msg.error {
        display: block;
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
        animation: authAlertPop 0.28s cubic-bezier(0.16, 1, 0.3, 1) both;
      }
      .auth-alert-msg.success {
        display: block;
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        animation: authAlertPop 0.28s cubic-bezier(0.16, 1, 0.3, 1) both;
      }
      @keyframes authAlertPop {
        from {
          opacity: 0;
          transform: translateY(-8px) scale(0.98);
        }
        to {
          opacity: 1;
          transform: translateY(0) scale(1);
        }
      }

      /* قائمة الملف الشخصي المنسدلة */
      .auth-profile-dropdown {
        position: absolute;
        top: calc(100% + 10px);
        left: 0;
        width: 290px;
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 18px;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6);
        display: block !important;
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        transform: translateY(10px) scale(0.95);
        transform-origin: top left;
        transition: opacity 0.22s cubic-bezier(0.16, 1, 0.3, 1),
                    transform 0.25s cubic-bezier(0.32, 0.72, 0, 1),
                    visibility 0.22s;
        z-index: 99999;
        direction: rtl;
        text-align: right;
        will-change: transform, opacity;
      }
      html.light .auth-profile-dropdown {
        background: #FFFFFF;
        border-color: rgba(15, 23, 42, 0.1);
        box-shadow: 0 20px 45px rgba(15, 23, 42, 0.15);
      }
      .auth-profile-dropdown.open {
        opacity: 1;
        visibility: visible;
        pointer-events: auto;
        transform: translateY(0) scale(1);
      }

      /* سلوك الهاتف المخصص: يظهر التمرير فقط عند صعود لوحة المفاتيح */
      @media (max-width: 640px) {
        .auth-modal-backdrop {
          padding: 8px;
          align-items: flex-end; /* يلتصق بأسفل الشاشة كـ Bottom Sheet */
          overflow-y: auto;
          -webkit-overflow-scrolling: touch;
        }
        .auth-modal-card {
          max-height: 94vh;
          overflow-y: auto; /* متاح للتمرير عند صعود اللوحة فقط */
          -webkit-overflow-scrolling: touch;
          border-radius: 22px 22px 14px 14px;
          padding: 20px 16px 24px;
          margin: 0 auto;
        }
        .auth-row-2 {
          grid-template-columns: 1fr;
          gap: 8px;
        }
        .auth-profile-dropdown {
          position: fixed !important;
          top: 60px !important;
          right: 12px !important;
          left: 12px !important;
          width: auto !important;
          max-width: calc(100vw - 24px) !important;
        }
      }

      /* نافذة إتاحة الميزات للطلاب المسجلين (Feature Gate VIP Modal) */
      .auth-gate-backdrop {
        position: fixed;
        inset: 0;
        background: rgba(15, 23, 42, 0.82);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        z-index: 100001;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 16px;
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        transition: opacity 0.28s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.28s;
      }
      .auth-gate-backdrop.open {
        opacity: 1;
        visibility: visible;
        pointer-events: auto;
      }
      .auth-gate-card {
        background: #0F172A;
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 24px;
        width: 100%;
        max-width: 480px;
        padding: 28px 24px 22px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8), 0 0 35px rgba(56, 189, 248, 0.15);
        transform: scale(0.92) translateY(16px);
        opacity: 0;
        transition: transform 0.32s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.26s ease;
        color: #F8FAFC;
        position: relative;
        direction: rtl;
        text-align: center;
        box-sizing: border-box;
      }
      html.light .auth-gate-card {
        background: #FFFFFF;
        border-color: rgba(2, 132, 199, 0.35);
        color: #0F172A;
        box-shadow: 0 25px 60px rgba(15, 23, 42, 0.15);
      }
      .auth-gate-backdrop.open .auth-gate-card {
        transform: scale(1) translateY(0);
        opacity: 1;
      }
      .gate-vip-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 800;
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.35);
        margin-bottom: 8px;
      }
      html.light .gate-vip-tag {
        background: rgba(217, 119, 6, 0.12);
        color: #B45309;
        
      border-color: rgba(217, 119, 6, 0.3);
    }

    /* شريط العينة المجانية في أعلى الأدوات */
    .guest-free-sample-banner {
      background: linear-gradient(90deg, rgba(56, 189, 248, 0.14), rgba(16, 185, 129, 0.14));
      border-bottom: 1px solid rgba(56, 189, 248, 0.28);
      padding: 9px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      font-size: 0.83rem;
      color: #F8FAFC;
      direction: rtl;
      position: relative;
      z-index: 999;
    }
    html.light .guest-free-sample-banner {
      background: linear-gradient(90deg, rgba(2, 132, 199, 0.09), rgba(5, 150, 105, 0.09));
      border-bottom-color: rgba(2, 132, 199, 0.22);
      color: #0F172A;
    }
    .sample-banner-text {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 600;
    }
    .sample-banner-btn {
      background: #10B981;
      color: #FFFFFF;
      border: none;
      border-radius: 9px;
      padding: 6px 14px;
      font-size: 0.8rem;
      font-weight: 800;
      cursor: pointer;
      white-space: nowrap;
      font-family: inherit;
      transition: transform 0.18s ease, box-shadow 0.2s ease, background-color 0.2s;
      box-shadow: 0 2px 10px rgba(16, 185, 129, 0.35);
    }
    .sample-banner-btn:hover {
      background: #059669;
      transform: translateY(-1px);
      box-shadow: 0 4px 14px rgba(16, 185, 129, 0.45);
    }
    @media (max-width: 640px) {
      .guest-free-sample-banner {
        flex-direction: column;
        text-align: center;
        gap: 8px;
        padding: 10px 14px;
      }
    }

    /* بطاقة المعاينة المقفولة */
    .locked-preview-card {
      position: relative;
      cursor: pointer;
      overflow: hidden;
      border-radius: 16px;
      transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .locked-preview-card:hover {
      transform: translateY(-2px);
    }
    .locked-preview-overlay {
      position: absolute;
      inset: 0;
      background: rgba(15, 23, 42, 0.78);
      backdrop-filter: blur(5px);
      -webkit-backdrop-filter: blur(5px);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 16px;
      z-index: 10;
      color: #FFF;
    }
    html.light .locked-preview-overlay {
      background: rgba(248, 250, 252, 0.85);
      color: #0F172A;
    }
    `;
    document.head.appendChild(style);
  }

  // 15. حقن نافذة تسجيل الدخول في الصفحة
  function injectAuthModalHtml() {
    if (document.getElementById('patenteAuthModal')) return;

    const modal = document.createElement('div');
    modal.className = 'auth-modal-backdrop';
    modal.id = 'patenteAuthModal';
    modal.innerHTML = `
      <div class="auth-modal-card" role="dialog" aria-modal="true">
        <button class="auth-close-btn" id="btnAuthClose" title="إغلاق">✕</button>

        <div style="text-align:center; margin-bottom:12px;">
          <div style="font-size:1.5rem; line-height:1.2; margin-bottom:2px;">🚦</div>
          <h2 style="font-size:1.15rem; font-weight:800; margin:0;" id="authModalTitle">تسجيل الدخول إلى Patente B Pro</h2>
          <p style="font-size:0.74rem; color:#94A3B8; margin:2px 0 0;" id="authModalSubtitle">احفظ إنجازك في السحابة وزامنه عبر جميع أجهزتك</p>
        </div>

        <div class="auth-tabs-nav" id="authTabsNav">
          <button class="auth-tab-btn active" id="tabBtnLogin">تسجيل الدخول</button>
          <button class="auth-tab-btn" id="tabBtnRegister">حساب جديد</button>
        </div>

        <div class="auth-alert-msg" id="authAlertMsg"></div>

        <!-- فورم تسجيل الدخول -->
        <form id="authLoginForm" class="auth-form-animated" autocomplete="on">
          <div class="auth-field-group">
            <label class="auth-label">البريد الإلكتروني</label>
            <input type="email" class="auth-input" id="loginEmail" placeholder="name@example.com" required dir="ltr" autocomplete="username">
          </div>
          <div class="auth-field-group">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <label class="auth-label">كلمة المرور</label>
              <a href="#" id="btnForgotPassword" style="font-size:0.75rem; color:#38BDF8; text-decoration:none;">نسيت كلمة المرور؟</a>
            </div>
            <input type="password" class="auth-input" id="loginPassword" placeholder="Password" required dir="ltr" autocomplete="current-password">
          </div>
          <button type="submit" class="auth-submit-btn" id="btnSubmitLogin">
            <span>تسجيل الدخول</span>
            <span>⬅</span>
          </button>
        </form>

        <!-- فورم إنشاء حساب جديد (مضغوط ومتناسق بدون سكرول على الديسكتوب) -->
        <form id="authRegisterForm" class="auth-form-animated" style="display:none;" autocomplete="off">
          <!-- الصف 1: الاسم الأول + اللقب -->
          <div class="auth-row-2">
            <div class="auth-field-group">
              <label class="auth-label">الاسم الأول</label>
              <input type="text" class="auth-input" id="regFirstName" placeholder="رامي" required autocomplete="off">
            </div>
            <div class="auth-field-group">
              <label class="auth-label">اللقب / العائلة</label>
              <input type="text" class="auth-input" id="regLastName" placeholder="المصري" required autocomplete="off">
            </div>
          </div>

          <!-- الصف 2: البريد الإلكتروني + كلمة المرور -->
          <div class="auth-row-2">
            <div class="auth-field-group">
              <label class="auth-label">البريد الإلكتروني <span style="color:#38BDF8; font-size:0.68rem;">(ستصلك رسالة تفعيل)</span></label>
              <input type="email" class="auth-input" id="regEmail" placeholder="name@example.com" required dir="ltr" autocomplete="off">
            </div>
            <div class="auth-field-group">
              <label class="auth-label">كلمة المرور</label>
              <input type="password" class="auth-input" id="regPassword" placeholder="Password" required minlength="6" dir="ltr" title="6 خانات على الأقل مع رمز خاص" autocomplete="new-password">
              <span style="font-size:0.68rem; color:#94A3B8; display:block; margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">💡 6+ خانات مع رمز خاص (@, #, $, %...)</span>
            </div>
          </div>

          <!-- الصف 3: الهاتف + تاريخ الميلاد -->
          <div class="auth-row-2">
            <div class="auth-field-group">
              <label class="auth-label">رقم الهاتف <span style="color:#38BDF8; font-size:0.68rem;">(حقيقي للتحقق)</span></label>
              <div style="display:flex; gap:6px; direction:ltr;">
                <select class="auth-select" id="regPhoneCountryCode" style="width:96px; flex-shrink:0; font-family:inherit; font-size:0.8rem; padding:0 4px;">
                  <option value="+39" selected>🇮🇹 +39</option>
                  <option value="+20">🇪🇬 +20</option>
                  <option value="+212">🇲🇦 +212</option>
                  <option value="+216">🇹🇳 +216</option>
                  <option value="+213">🇩🇿 +213</option>
                  <option value="+218">🇱🇾 +218</option>
                  <option value="+249">🇸🇩 +249</option>
                  <option value="+966">🇸🇦 +966</option>
                  <option value="+971">🇦🇪 +971</option>
                  <option value="+49">🇩🇪 +49</option>
                  <option value="+33">🇫🇷 +33</option>
                  <option value="+34">🇪🇸 +34</option>
                  <option value="+41">🇨🇭 +41</option>
                  <option value="+44">🇬🇧 +44</option>
                  <option value="">🌍 أخرى</option>
                </select>
                <input type="tel" class="auth-input" id="regPhone" placeholder="345 123 4567" style="flex:1;" dir="ltr" required autocomplete="off">
              </div>
            </div>
            <div class="auth-field-group">
              <label class="auth-label">تاريخ الميلاد</label>
              <input type="date" class="auth-input" id="regBirthDate" required autocomplete="off">
            </div>
          </div>

          <!-- الصف 4: النوع -->
          <div class="auth-field-group">
            <label class="auth-label">النوع</label>
            <select class="auth-select" id="regGender" required>
              <option value="male">ذكر (Maschio)</option>
              <option value="female">أنثى (Femmina)</option>
              <option value="other">غير محدد / أفضل عدم الإفصاح (Altro / Non specificato)</option>
            </select>
          </div>

          <button type="submit" class="auth-submit-btn" id="btnSubmitRegister">
            <span>إنشاء الحساب ومزامنة الإنجاز</span>
            <span>🎉</span>
          </button>
        </form>

        <!-- شاشة تأكيد البريد الإلكتروني الفاخرة (Apple HIG Verification Screen) -->
        <div id="authVerifyScreen" style="display:none; text-align:center; padding:6px 2px;" class="auth-form-animated">
          <div style="font-size:2.8rem; line-height:1; margin-bottom:8px;">✉️</div>
          <h3 style="font-size:1.18rem; font-weight:800; color:#10B981; margin:0 0 6px;">تم إنشاء حسابك بنجاح! 🎉</h3>
          <p style="font-size:0.83rem; color:#94A3B8; margin:0 0 12px; line-height:1.6;">
            أرسلنا رابط التحقق والتفعيل فوراً إلى بريدك الإلكتروني:<br>
            <strong id="verifyScreenEmail" style="color:#38BDF8; font-size:0.92rem;" dir="ltr">name@example.com</strong>
          </p>

          <div style="background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.25); border-radius:14px; padding:12px 14px; font-size:0.79rem; color:#CBD5E1; margin-bottom:14px; text-align:right; line-height:1.7;">
            <div style="font-weight:800; color:#38BDF8; margin-bottom:4px;">📌 خطوة واحدة لتفعيل حسابك والدخول:</div>
            1. افتح تطبيق البريد الإلكتروني (Inbox ومجلد Spam / غير المرغوب فيها).<br>
            2. افتح رسالة <strong>Google Firebase</strong> واضغط على رابط التفعيل المرفق.<br>
            3. عد إلى هنا وسجل دخولك لتجد كافة ميزاتك وتقدمك بانتظارك.
          </div>

          <button type="button" class="auth-submit-btn" id="btnVerifyGoLogin" style="margin-top:0;">
            <span>التوجه إلى تسجيل الدخول</span>
            <span>⬅</span>
          </button>

          <div style="margin-top:10px;">
            <button type="button" id="btnResendFromVerifyScreen" style="background:transparent; border:none; color:#38BDF8; font-size:0.78rem; font-weight:700; cursor:pointer; font-family:inherit; text-decoration:underline;">
              لم تصلك الرسالة؟ اضغط لإعادة إرسال الرابط 🔄
            </button>
          </div>
        </div>

        <!-- فاصل أو الدخول بجوجل -->
        <div id="authGoogleDivider" style="display:flex; align-items:center; gap:10px; margin:10px 0 6px;">
          <div style="flex:1; height:1px; background:rgba(255,255,255,0.1);"></div>
          <span style="font-size:0.75rem; color:#64748B;">أو عبر</span>
          <div style="flex:1; height:1px; background:rgba(255,255,255,0.1);"></div>
        </div>

        <button type="button" class="auth-google-btn" id="btnGoogleAuth">
          <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.66v3.05h3.88c2.27-2.09 3.665-5.17 3.665-9.15z"/><path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.35 24 12 24z"/><path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.17 0 9.98 0 12s.45 3.83 1.25 5.42l4.03-3.15z"/><path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.35 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"/></svg>
          <span>المتابعة باستخدام Google</span>
        </button>
      </div>
    `;

    document.body.appendChild(modal);
    wireAuthModalEvents();
  }

  // 16. ربط أحداث النوافذ والأزرار
  function wireAuthModalEvents() {
    const modal = document.getElementById('patenteAuthModal');
    const closeBtn = document.getElementById('btnAuthClose');
    const tabLogin = document.getElementById('tabBtnLogin');
    const tabReg = document.getElementById('tabBtnRegister');
    const formLogin = document.getElementById('authLoginForm');
    const formReg = document.getElementById('authRegisterForm');
    const verifyScreen = document.getElementById('authVerifyScreen');
    const tabsNav = document.getElementById('authTabsNav');
    const googleDivider = document.getElementById('authGoogleDivider');
    const googleBtn = document.getElementById('btnGoogleAuth');
    const titleEl = document.getElementById('authModalTitle');
    const subtitleEl = document.getElementById('authModalSubtitle');
    const alertBox = document.getElementById('authAlertMsg');

    function showAlert(msg, isSuccess = false, isHtml = false) {
      if (isHtml) {
        alertBox.innerHTML = msg;
      } else {
        alertBox.textContent = msg;
      }
      alertBox.className = 'auth-alert-msg ' + (isSuccess ? 'success' : 'error');
    }

    function clearAlert() {
      alertBox.textContent = '';
      alertBox.className = 'auth-alert-msg';
    }

    closeBtn.onclick = () => modal.classList.remove('open');

    // إغلاق آمن عند النقر على الخلفية بدون إغلاق بالخطأ أثناء سحب التمرير
    let isMouseDownOnBackdrop = false;
    modal.addEventListener('mousedown', (e) => {
      isMouseDownOnBackdrop = (e.target === modal);
    });
    modal.addEventListener('mouseup', (e) => {
      if (isMouseDownOnBackdrop && e.target === modal) {
        modal.classList.remove('open');
      }
      isMouseDownOnBackdrop = false;
    });

    // التنقل الانسيابي الفاخر بين تبويبي الدخول والحساب الجديد
    function switchTab(toRegister) {
      clearAlert();
      const card = modal.querySelector('.auth-modal-card');

      // إعادة إظهار التبويبات والفاصل إن كانت مخفية بشاشة التأكيد
      if (verifyScreen) verifyScreen.style.display = 'none';
      if (tabsNav) tabsNav.style.display = 'flex';
      if (googleDivider) googleDivider.style.display = 'flex';
      if (googleBtn) googleBtn.style.display = 'flex';
      if (subtitleEl) subtitleEl.style.display = 'block';

      if (toRegister) {
        tabReg.classList.add('active');
        tabLogin.classList.remove('active');
        formLogin.style.display = 'none';
        formReg.style.display = 'block';
        const regPass = document.getElementById('regPassword');
        if (regPass) regPass.value = '';
        formReg.classList.remove('auth-form-animated');
        void formReg.offsetWidth; // إجبار المتصفح على إعادة تطبيق حركة الدخول
        formReg.classList.add('auth-form-animated');
        if (titleEl) titleEl.textContent = 'إنشاء حساب جديد في Patente B Pro';
      } else {
        tabLogin.classList.add('active');
        tabReg.classList.remove('active');
        formReg.style.display = 'none';
        formLogin.style.display = 'block';
        const loginPass = document.getElementById('loginPassword');
        if (loginPass) loginPass.value = '';
        formLogin.classList.remove('auth-form-animated');
        void formLogin.offsetWidth;
        formLogin.classList.add('auth-form-animated');
        if (titleEl) titleEl.textContent = 'تسجيل الدخول إلى Patente B Pro';
      }

      // تمرير ناعم لأعلى البطاقة عند التبديل
      if (card) {
        card.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }

    tabLogin.onclick = () => switchTab(false);
    tabReg.onclick = () => switchTab(true);

    // زر التوجه للدخول من شاشة التأكيد
    const btnVerifyGoLogin = document.getElementById('btnVerifyGoLogin');
    if (btnVerifyGoLogin) {
      btnVerifyGoLogin.onclick = () => {
        switchTab(false);
        if (lastRegisteredCredentials && lastRegisteredCredentials.email) {
          const loginEmailInput = document.getElementById('loginEmail');
          if (loginEmailInput) loginEmailInput.value = lastRegisteredCredentials.email;
          const loginPassInput = document.getElementById('loginPassword');
          if (loginPassInput) {
            loginPassInput.value = '';
            loginPassInput.focus();
          }
        }
      };
    }

    // زر إعادة إرسال الرابط من شاشة التأكيد
    const btnResendFromVerify = document.getElementById('btnResendFromVerifyScreen');
    if (btnResendFromVerify) {
      btnResendFromVerify.onclick = async () => {
        btnResendFromVerify.disabled = true;
        btnResendFromVerify.textContent = 'جاري إعادة الإرسال... ⏳';
        try {
          await resendVerificationEmail(
            lastRegisteredCredentials ? lastRegisteredCredentials.email : '',
            lastRegisteredCredentials ? lastRegisteredCredentials.password : ''
          );
          btnResendFromVerify.textContent = '✅ تم إرسال رابط تأكيد جديد إلى بريدك!';
          showAlert('✅ تم إرسال رابط تأكيد جديد إلى بريدك بنجاح! تفقد بريدك الآن.', true);
          setTimeout(() => {
            btnResendFromVerify.disabled = false;
            btnResendFromVerify.textContent = 'لم تصلك الرسالة؟ اضغط لإعادة إرسال الرابط 🔄';
          }, 4000);
        } catch (e) {
          btnResendFromVerify.disabled = false;
          btnResendFromVerify.textContent = 'لم تصلك الرسالة؟ اضغط لإعادة إرسال الرابط 🔄';
          showAlert('تعذر إعادة الإرسال: ' + translateFirebaseError(e.code || e.message));
        }
      };
    }

    // على الهواتف: عند ظهور لوحة المفاتيح والتركيز في أي حقل، يتم التمرير بسلاسة ليبقى الحقل ظاهراً في المنتصف
    modal.addEventListener('focusin', (e) => {
      if (window.innerWidth <= 640 && e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT')) {
        setTimeout(() => {
          e.target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 220);
      }
    });

    // إرسال تسجيل الدخول
    formLogin.onsubmit = async (e) => {
      e.preventDefault();
      clearAlert();
      const email = document.getElementById('loginEmail').value;
      const pass = document.getElementById('loginPassword').value;
      const submitBtn = document.getElementById('btnSubmitLogin');

      submitBtn.disabled = true;
      submitBtn.innerHTML = 'جاري التحقق... ⏳';

      try {
        await loginAccount(email, pass);
        showAlert('تم تسجيل الدخول بنجاح! مرحباً بك 🚀', true);
        setTimeout(() => modal.classList.remove('open'), 900);
      } catch (err) {
        if (err && err.code === 'auth/email-not-verified') {
          // عرض تنبيه تفاعلي أنيق مع زر لإعادة إرسال الرابط فوراً
          const htmlMsg = `
            <div style="text-align:right; line-height:1.6;">
              <div style="font-weight:800; margin-bottom:4px; color:#F87171;">⚠️ هذا الحساب غير مفعل بعد!</div>
              أرسلنا رابط التفعيل إلى بريدك الإلكتروني. يرجى الضغط على الرابط في رسالتك لتفعيل الحساب لتتمكن من تسجيل الدخول.
              <div style="margin-top:8px;">
                <button type="button" id="btnResendFromLoginAlert" style="background:#38BDF8; color:#0F172A; border:none; border-radius:7px; padding:5px 12px; font-weight:800; font-size:0.77rem; cursor:pointer; font-family:inherit;">
                  📧 إعادة إرسال رابط التفعيل الآن
                </button>
              </div>
            </div>
          `;
          showAlert(htmlMsg, false, true);

          const alertResendBtn = document.getElementById('btnResendFromLoginAlert');
          if (alertResendBtn) {
            alertResendBtn.onclick = async () => {
              alertResendBtn.disabled = true;
              alertResendBtn.textContent = 'جاري الإرسال... ⏳';
              try {
                await resendVerificationEmail(email, pass);
                showAlert('✅ تم إعادة إرسال رابط التفعيل إلى بريدك بنجاح! يرجى فحص صندوق الوارد أو Spam.', true);
              } catch (resendErr) {
                showAlert('تعذر إرسال الرابط: ' + translateFirebaseError(resendErr.code || resendErr.message));
              }
            };
          }
        } else {
          showAlert(translateFirebaseError(err.code || err.message));
        }
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<span>تسجيل الدخول</span> <span>⬅</span>';
      }
    };

    // إرسال إنشاء الحساب
    formReg.onsubmit = async (e) => {
      e.preventDefault();
      clearAlert();

      const firstName = (document.getElementById('regFirstName').value || '').trim();
      const lastName = (document.getElementById('regLastName').value || '').trim();
      if (!firstName || !lastName) {
        showAlert('يرجى كتابة الاسم الأول واللقب.');
        return;
      }

      const email = (document.getElementById('regEmail').value || '').trim();
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        showAlert('يرجى إدخال عنوان بريد إلكتروني صالح (مثال: name@example.com).');
        return;
      }

      const password = (document.getElementById('regPassword').value || '');
      const specialCharRegex = /[^a-zA-Z0-9\s]/;
      if (password.length < 6 || !specialCharRegex.test(password)) {
        showAlert('كلمة المرور يجب أن تتكون من 6 خانات على الأقل وتتضمن رمزاً خاصاً واحداً على الأقل (مثل: @, #, $, %, !, -, *, +, §)');
        return;
      }

      const phoneCode = document.getElementById('regPhoneCountryCode') ? document.getElementById('regPhoneCountryCode').value : '+39';
      const rawPhone = (document.getElementById('regPhone').value || '').trim();
      const phoneDigits = rawPhone.replace(/\D/g, '');
      if (!rawPhone || phoneDigits.length < 7 || phoneDigits.length > 15) {
        showAlert('يرجى إدخال رقم هاتف صحيح مكوّن من 7 إلى 15 رقماً.');
        return;
      }
      const combinedPhone = phoneCode ? `${phoneCode} ${rawPhone}`.trim() : rawPhone;

      const birthDate = document.getElementById('regBirthDate').value;
      if (!birthDate) {
        showAlert('يرجى تحديد تاريخ الميلاد.');
        return;
      }

      const submitBtn = document.getElementById('btnSubmitRegister');

      const data = {
        firstName: firstName,
        lastName: lastName,
        email: email,
        password: password,
        phone: combinedPhone,
        birthDate: birthDate,
        gender: document.getElementById('regGender').value
      };

      submitBtn.disabled = true;
      submitBtn.innerHTML = 'جاري إنشاء الحساب وإرسال رابط التفعيل... ⏳';

      try {
        const result = await registerAccount(data);
        lastRegisteredCredentials = { email: data.email, password: data.password };

        // تحويل الواجهة فوراً لشاشة تأكيد البريد الإلكتروني (Apple HIG Verification Screen)
        formReg.style.display = 'none';
        if (tabsNav) tabsNav.style.display = 'none';
        if (googleDivider) googleDivider.style.display = 'none';
        if (googleBtn) googleBtn.style.display = 'none';
        if (subtitleEl) subtitleEl.style.display = 'none';

        if (titleEl) titleEl.textContent = 'تأكيد البريد الإلكتروني';
        const verifyEmailSpan = document.getElementById('verifyScreenEmail');
        if (verifyEmailSpan) verifyEmailSpan.textContent = result.email;
        if (verifyScreen) verifyScreen.style.display = 'block';

        const card = modal.querySelector('.auth-modal-card');
        if (card) card.scrollTo({ top: 0, behavior: 'smooth' });

      } catch (err) {
        showAlert(translateFirebaseError(err.code || err.message));
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<span>إنشاء الحساب ومزامنة الإنجاز</span> <span>🎉</span>';
      }
    };

    // الدخول بجوجل مع معالجة ذكية لحظر النوافذ المنبثقة
    document.getElementById('btnGoogleAuth').onclick = async () => {
      clearAlert();
      const btn = document.getElementById('btnGoogleAuth');
      try {
        btn.disabled = true;
        btn.style.opacity = '0.7';
        btn.innerHTML = '<span>جاري الاتصال بـ Google... ⏳</span>';
        const user = await loginWithGoogle();
        if (user) {
          showAlert('تم الدخول بنجاح بحساب Google! 🎉', true);
          setTimeout(() => modal.classList.remove('open'), 900);
        } else {
          // في حال تم تفعيل التحويل المباشر (Redirect Flow)
          showAlert('جاري تحويلك إلى صفحة تسجيل الدخول بحساب Google... ⏳', true);
        }
      } catch (err) {
        showAlert(translateFirebaseError(err.code || err.message));
      } finally {
        btn.disabled = false;
        btn.style.opacity = '1';
        btn.innerHTML = `
          <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.66v3.05h3.88c2.27-2.09 3.665-5.17 3.665-9.15z"/><path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.35 24 12 24z"/><path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.17 0 9.98 0 12s.45 3.83 1.25 5.42l4.03-3.15z"/><path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.35 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"/></svg>
          <span>المتابعة باستخدام Google</span>
        `;
      }
    };

    // نسيت كلمة المرور
    document.getElementById('btnForgotPassword').onclick = async (e) => {
      e.preventDefault();
      const email = document.getElementById('loginEmail').value;
      if (!email) {
        showAlert('يرجى كتابة بريدك الإلكتروني في الحقل أولاً لإرسال رابط الاسترجاع.');
        return;
      }
      try {
        await resetPassword(email);
        showAlert('تم إرسال رابط استعادة كلمة المرور إلى بريدك الإلكتروني بنجاح! 📧', true);
      } catch (err) {
        showAlert(translateFirebaseError(err.code || err.message));
      }
    };
  }

  // 17. ترجمة أخطاء Firebase للعربية بشكل مفهوم
  function translateFirebaseError(code) {
    if (!code) return 'حدث خطأ غير متوقع، يرجى المحاولة مرة أخرى.';
    if (code.includes('email-not-verified')) {
      return '⚠️ لم يتم تفعيل حسابك بعد! أرسلنا رابط التفعيل إلى بريدك الإلكتروني. يرجى فتح الرسالة وتأكيد حسابك لتتمكن من الدخول.';
    }
    if (code.includes('too-many-requests')) {
      return 'تم تعطيل المحاولات مؤقتاً لكثرة الطلبات. يرجى الانتظار بضع دقائق والمحاولة مجدداً.';
    }
    if (code.includes('quota-exceeded')) {
      return 'تم تجاوز الحد الأقصى المسموح به في السحابة حالياً.';
    }
    if (code.includes('user-not-found') || code.includes('wrong-password') || code.includes('invalid-credential')) {
      return 'البريد الإلكتروني أو كلمة المرور غير صحيحة.';
    }
    if (code.includes('email-already-in-use')) {
      return 'هذا البريد الإلكتروني مسجل بالفعل بحساب آخر.';
    }
    if (code.includes('invalid-email')) {
      return 'صيغة البريد الإلكتروني غير صالحة.';
    }
    if (code.includes('weak-password')) {
      return 'كلمة المرور ضعيفة جداً. يجب أن تحتوي على 6 خانات على الأقل وتتضمن رمزاً خاصاً.';
    }
    if (code.includes('popup-blocked')) {
      return 'قام المتصفح بحظر النافذة المنبثقة. جاري تحويلك إلى صفحة الدخول المباشرة...';
    }
    if (code.includes('popup-closed-by-user')) {
      return 'تم إلغاء نافذة الدخول بواسطة المستخدم.';
    }
    if (code.includes('api-key-not-valid') || code.includes('invalid-api-key')) {
      return 'مفتاح التهيئة السحابي غير صالح. يرجى مراجعة إعدادات Firebase.';
    }
    if (code.includes('unauthorized-domain')) {
      const host = window.location.hostname;
      if (!host || window.location.protocol === 'file:') {
        return 'المصادقة السحابية تتطلب تشغيل الموقع عبر خادم محلي (localhost) أو استضافة، ولا تعمل عبر فتح الملف مباشرة (file://). يرجى تشغيل ملف run_local_server.bat المرفق.';
      }
      return `النطاق الحالي (${host}) غير مصرح به في Firebase. يرجى إضافته في إعدادات المشروع (Authorized domains).`;
    }
    return code;
  }

  // 18. تحديث واجهة المستخدم عند تسجيل الخروج (Guest Mode)
  function updateAuthUiLoggedOut() {
    const pill = document.getElementById('globalAuthPill');
    if (pill) {
      pill.className = 'nav-auth-pill guest';
      pill.innerHTML = '<span>👤</span> <span>دخول / تسجيل</span>';
      pill.title = 'تسجيل الدخول أو إنشاء حساب جديد لحفظ تقدمك سحابياً';
      pill.onclick = () => {
        document.getElementById('patenteAuthModal').classList.add('open');
      };
    }

    const mobBtn = document.getElementById('btnOpenMobileAuth');
    if (mobBtn) {
      mobBtn.classList.remove('logged-in');
      mobBtn.title = 'دخول / تسجيل';
      mobBtn.onclick = () => {
        document.getElementById('patenteAuthModal').classList.add('open');
      };
    }

    const drop = document.getElementById('authProfileDropdown');
    if (drop) drop.classList.remove('open');
  }

  // 19. تحديث واجهة المستخدم عند تسجيل الدخول (Logged In)
  function updateAuthUiLoggedIn(profile) {
    const active = userProfile || profile || {};
    const pill = document.getElementById('globalAuthPill');
    const name = active.firstName || active.displayName || (active.email ? active.email.split('@')[0] : 'طالب');

    if (pill) {
      pill.className = 'nav-auth-pill logged-in';
      pill.innerHTML = `
        <span class="auth-online-dot" id="authSyncDot"></span>
        <span>👤 ${escapeHtml(name)}</span>
        <span style="font-size:0.7rem;">▾</span>
      `;
      pill.title = `مسجل كـ: ${active.email || ''} (انقر لعرض الملف الشخصي والمزامنة)`;
      pill.onclick = (e) => {
        e.stopPropagation();
        toggleProfileDropdown(userProfile || profile);
      };
    }

    const mobBtn = document.getElementById('btnOpenMobileAuth');
    if (mobBtn) {
      mobBtn.classList.add('logged-in');
      mobBtn.title = `مسجل كـ: ${active.email || ''}`;
      mobBtn.onclick = (e) => {
        e.stopPropagation();
        toggleProfileDropdown(userProfile || profile);
      };
    }
  }

  // 20. إدارة القائمة المنسدلة للملف الشخصي (Profile Dropdown)
  function toggleProfileDropdown(profile) {
    const active = userProfile || profile || {};
    let drop = document.getElementById('authProfileDropdown');
    const pill = document.getElementById('globalAuthPill');
    const mobBtn = document.getElementById('btnOpenMobileAuth');
    const parentContainer = (pill && pill.parentElement) || (mobBtn && mobBtn.parentElement) || document.body;

    if (!drop) {
      drop = document.createElement('div');
      drop.className = 'auth-profile-dropdown';
      drop.id = 'authProfileDropdown';
      parentContainer.appendChild(drop);
    }

    const isCurrentlyOpen = drop.classList.contains('open');
    if (isCurrentlyOpen) {
      drop.classList.remove('open');
      return;
    }

    const fullName = active.fullName || `${active.firstName || ''} ${active.lastName || ''}`.trim() || active.displayName || 'طالب رخصة القيادة';
    const email = active.email || (currentUser ? currentUser.email : '');
    const phone = active.phone || 'غير مسجل';
    const bdate = active.birthDate || 'غير مسجل';
    const genderStr = active.gender === 'male' ? 'ذكر 👨' : active.gender === 'female' ? 'أنثى 👩' : 'غير محدد / آخر 👤';
    const firstLetter = (active.firstName || active.fullName || 'ط').trim().charAt(0).toUpperCase();

    drop.innerHTML = `
      <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px; padding-bottom:12px; border-bottom:1px solid rgba(255,255,255,0.08);">
        <div style="width:42px; height:42px; border-radius:50%; background:#10B981; color:#FFF; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.1rem; flex-shrink:0;">
          ${escapeHtml(firstLetter)}
        </div>
        <div style="overflow:hidden; flex:1;">
          <div style="font-weight:800; font-size:0.95rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${escapeHtml(fullName)}</div>
          <div style="font-size:0.75rem; color:#94A3B8; direction:ltr; text-align:right; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${escapeHtml(email)}</div>
        </div>
      </div>

      <div style="font-size:0.78rem; color:#94A3B8; margin-bottom:12px; line-height:1.7;">
        <div>📱 <strong>الهاتف:</strong> <span dir="ltr">${escapeHtml(phone)}</span></div>
        <div>🎂 <strong>الميلاد:</strong> ${escapeHtml(bdate)}</div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div>👤 <strong>النوع:</strong> ${genderStr}</div>
          <button id="btnDeleteAccountInline" title="حذف الحساب وجميع البيانات نهائياً من السحابة" style="background:transparent; border:none; color:#EF4444; font-size:0.72rem; cursor:pointer; padding:1px 4px; border-radius:4px; opacity:0.8; font-family:inherit; transition:all 0.2s; display:inline-flex; align-items:center; gap:3px;">
            <span>🗑️</span>
            <span>حذف الحساب</span>
          </button>
        </div>
      </div>

      <div style="background:rgba(255,255,255,0.04); border-radius:10px; padding:10px; margin-bottom:12px; font-size:0.75rem;">
        <div id="dropdownSyncStatusText" style="color:#34D399; font-weight:700;">🟢 الحساب متصل ومتزامن سحابياً</div>
        <div style="color:#64748B; font-size:0.7rem; margin-top:2px;">يتم حفظ تقدمك تلقائياً بعد كل باب وامتحان.</div>
      </div>

      <button id="btnManualSyncNow" style="width:100%; height:36px; border-radius:10px; background:rgba(56,189,248,0.12); border:1px solid rgba(56,189,248,0.3); color:#38BDF8; font-weight:700; font-size:0.82rem; cursor:pointer; font-family:inherit; margin-bottom:8px; display:flex; align-items:center; justify-content:center; gap:6px;">
        <span>🔄 مزامنة سحابية فورية الآن</span>
      </button>

      <button id="btnAuthLogout" style="width:100%; height:36px; border-radius:10px; background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.3); color:#EF4444; font-weight:700; font-size:0.82rem; cursor:pointer; font-family:inherit; display:flex; align-items:center; justify-content:center; gap:6px;">
        <span>🚪 تسجيل الخروج</span>
      </button>
    `;

    drop.classList.add('open');

    // زر المزامنة الفورية
    document.getElementById('btnManualSyncNow').onclick = async () => {
      const btn = document.getElementById('btnManualSyncNow');
      btn.innerHTML = 'جاري المزامنة... ⏳';
      btn.disabled = true;
      if (currentUser && currentUser.uid) {
        await uploadLocalProgressToCloud(currentUser.uid);
      }
      btn.innerHTML = '✅ تمت المزامنة بنجاح!';
      setTimeout(() => {
        btn.innerHTML = '<span>🔄 مزامنة سحابية فورية الآن</span>';
        btn.disabled = false;
      }, 1500);
    };

    // زر تسجيل الخروج
    document.getElementById('btnAuthLogout').onclick = async () => {
      if (confirm('هل تريد تسجيل الخروج من حسابك؟')) {
        await logoutAccount();
        drop.classList.remove('open');
      }
    };

    // زر حذف الحساب نهائياً (الموجود في قسم البيانات)
    const delBtn = document.getElementById('btnDeleteAccountInline');
    if (delBtn) {
      delBtn.onclick = async () => {
        const confirmed = confirm(
          '⚠️ تحذير نهائي:\n\n' +
          'هل أنت متأكد تماماً من حذف حسابك وكافة سجلاتك وتقدمك السحابي نهائياً؟\n\n' +
          '• سيتم مسح ملفك وجميع سجلاتك من خوادم السحابة فوراً.\n' +
          '• لن تتمكن من استرجاع تقدمك في الأسئلة أو الامتحانات بعد الحذف.\n' +
          '• يمكنك إنشاء حساب جديد بنفس البريد لاحقاً في أي وقت.'
        );
        if (!confirmed) return;

        delBtn.innerHTML = 'جاري الحذف... ⏳';
        delBtn.disabled = true;

        try {
          await deleteCurrentAccount();
          drop.classList.remove('open');
          alert('✅ تم حذف حسابك وكافة بياناتك السحابية نهائياً بنجاح.');
        } catch (err) {
          delBtn.innerHTML = '<span>🗑️</span> <span>حذف الحساب</span>';
          delBtn.disabled = false;
          if (err && err.code === 'auth/requires-recent-login') {
            alert('🔒 لأسباب أمنية مشددة، يتطلب حذف الحساب إعادة تسجيل الدخول حديثاً. يرجى تسجيل الخروج ثم الدخول مرة أخرى والمحاولة مجدداً.');
          } else {
            alert('تعذر حذف الحساب حالياً: ' + ((err && err.message) || 'يرجى المحاولة لاحقاً.'));
          }
        }
      };
    }

    // إغلاق عند النقر بالخارج
    const closeListener = (evt) => {
      if (!drop.contains(evt.target) && evt.target !== pill && (!mobBtn || !mobBtn.contains(evt.target))) {
        drop.classList.remove('open');
        document.removeEventListener('click', closeListener);
      }
    };
    setTimeout(() => document.addEventListener('click', closeListener), 10);
  }

  function updateSyncIndicator(isSync) {
    const dot = document.getElementById('authSyncDot');
    if (dot) {
      dot.className = isSync ? 'auth-online-dot syncing' : 'auth-online-dot';
    }
  }

  function updateSyncStatusText(text) {
    const el = document.getElementById('dropdownSyncStatusText');
    if (el) el.textContent = text;
  }

  // 21. التحقق من حالة الدخول وبوابة الميزات المتقدمة (Feature Gating)
  function isUserLoggedIn() {
    if (!currentUser) return false;
    const isGoogle = currentUser.providerData && currentUser.providerData.some(p => p.providerId === 'google.com');
    if (!isGoogle && !currentUser.emailVerified) {
      return false;
    }
    return true;
  }

  function injectGateModalHtml() {
    if (document.getElementById('patenteGateModal')) return;

    const gate = document.createElement('div');
    gate.className = 'auth-gate-backdrop';
    gate.id = 'patenteGateModal';
    gate.innerHTML = `
      <div class="auth-gate-card" role="dialog" aria-modal="true">
        <button class="auth-close-btn" id="btnGateClose" title="إغلاق">✕</button>
        <div style="font-size:2.6rem; line-height:1; margin-bottom:8px;">👑</div>
        <span class="gate-vip-tag" id="gateModalBadge">ميزة حصرية للطلاب</span>
        <h3 id="gateModalTitle" style="font-size:1.22rem; font-weight:800; margin:10px 0 8px; color:inherit;">
          هذه الميزة متاحة مجاناً للطلاب المسجلين!
        </h3>
        <p id="gateModalDesc" style="font-size:0.86rem; color:#94A3B8; margin:0 0 20px; line-height:1.65;">
          لقد شاهدت عينة مجانية من هذه الأداة. أنشئ حسابك المجاني في ثوانٍ لفتح جميع المحتويات وحفظ أخطائك وإنجازك سحابياً عبر كل أجهزتك.
        </p>
        <div style="display:flex; flex-direction:column; gap:8px;">
          <button id="btnGateRegister" class="auth-submit-btn" style="margin-top:0; height:42px; font-size:0.92rem;">
            <span>🚀 إنشاء حساب مجاني الآن</span>
          </button>
          <button id="btnGateDismiss" style="height:36px; border-radius:10px; background:transparent; border:1px solid rgba(255,255,255,0.12); color:#94A3B8; font-weight:600; cursor:pointer; font-size:0.82rem; font-family:inherit;">
            <span>متابعة التصفح كزائر</span>
          </button>
        </div>
      </div>
    `;

    document.body.appendChild(gate);

    const closeBtn = document.getElementById('btnGateClose');
    const dismissBtn = document.getElementById('btnGateDismiss');
    const regBtn = document.getElementById('btnGateRegister');

    const closeGate = () => gate.classList.remove('open');
    if (closeBtn) closeBtn.onclick = closeGate;
    if (dismissBtn) dismissBtn.onclick = closeGate;
    gate.onclick = (e) => {
      if (e.target === gate) closeGate();
    };

    if (regBtn) {
      regBtn.onclick = () => {
        closeGate();
        openAuthModal(true);
      };
    }
  }

  function showGateModal(options = {}) {
    injectGateModalHtml();
    const modal = document.getElementById('patenteGateModal');
    if (!modal) return;

    const titleEl = document.getElementById('gateModalTitle');
    const descEl = document.getElementById('gateModalDesc');
    const badgeEl = document.getElementById('gateModalBadge');

    if (titleEl && options.title) titleEl.textContent = options.title;
    if (descEl && options.message) descEl.textContent = options.message;
    if (badgeEl && options.badge) badgeEl.textContent = options.badge;

    modal.classList.add('open');
  }

  function requireAuth(options = {}) {
    if (isUserLoggedIn()) return true;
    showGateModal(options);
    return false;
  }

  function openAuthModal(openRegisterTab = false) {
    const modal = document.getElementById('patenteAuthModal');
    if (modal) {
      if (openRegisterTab) {
        clearAuthForms();
        modal.classList.add('open');
        const tabReg = document.getElementById('tabBtnRegister');
        if (tabReg) tabReg.click();
      } else {
        modal.classList.add('open');
      }
    }
  }

  // 22. الواجهة البرمجية العامة المعرضة للتطبيق (Global API)
  window.PatenteAuth = {
    init: initFirebase,
    register: registerAccount,
    login: loginAccount,
    loginWithGoogle: loginWithGoogle,
    logout: logoutAccount,
    deleteAccount: deleteCurrentAccount,
    resetPassword: resetPassword,
    resendVerificationEmail: resendVerificationEmail,
    syncToCloud: () => currentUser ? uploadLocalProgressToCloud(currentUser.uid) : Promise.resolve(),
    pullFromCloud: () => currentUser ? pullCloudProgressToLocal(currentUser.uid) : Promise.resolve(),
    getCurrentUser: () => currentUser,
    getUserProfile: () => userProfile,
    isLoggedIn: isUserLoggedIn,
    showGateModal: showGateModal,
    requireAuth: requireAuth,
    openAuthModal: openAuthModal
  };

  // تهيئة وتشغيل المحرك فورياً
  function startEngine() {
    injectAuthStyles();
    injectAuthModalHtml();
    injectGateModalHtml();
    initFirebase();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startEngine);
  } else {
    startEngine();
  }

})();
