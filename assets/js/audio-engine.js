/**
 * =======================================================================
 * Patente B Pro - Bilingual Audio Glossary & Pronunciation Engine
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description محرك المسرد الصوتي المزدوج والنطق الإيطالي:
 *  - النطق الإيطالي الصوتي النقي للمصطلحات عبر Web Speech API (مع Fallback لـ Web Audio)
 *  - دعم النطق الفونيتيكي الصوتي بالعربية لمساعدة الطلاب في القراءة
 *  - محرك توليد نغمات تفاعلية للنقر والإجابات الصحيحة والخاطئة
 */

class PatenteAudioEngine {
  constructor() {
    this.speechSynthesis = typeof window !== "undefined" ? window.speechSynthesis : null;
    this.audioCtx = null;
    this.italianVoice = null;
    this.isMuted = false;

    this.initVoices();
  }

  /**
   * تهيئة الصوت الإيطالي من أصوات النظام
   */
  initVoices() {
    if (!this.speechSynthesis) return;

    const setVoice = () => {
      const voices = this.speechSynthesis.getVoices();
      // البحث عن صوت إيطالي طبيعي
      this.italianVoice = voices.find((v) => v.lang.startsWith("it") || v.lang.includes("it-IT")) || null;
    };

    setVoice();
    if (this.speechSynthesis.onvoiceschanged !== undefined) {
      this.speechSynthesis.onvoiceschanged = setVoice;
    }
  }

  /**
   * تهيئة سياق الصوت التفاعلي (Web Audio API) عند أول تفاعل من المستخدم
   */
  ensureAudioContext() {
    if (!this.audioCtx && typeof window !== "undefined") {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.audioCtx = new AudioContext();
      }
    }
    if (this.audioCtx && this.audioCtx.state === "suspended") {
      this.audioCtx.resume();
    }
  }

  /**
   * نطق المصطلح الإيطالي بصوت واضح
   * @param {string} text النص الإيطالي
   * @param {number} rate سرعة النطق (0.85 مثالية للتعلم)
   */
  speakItalian(text, rate = 0.85) {
    if (!this.speechSynthesis || this.isMuted || !text) return;

    this.speechSynthesis.cancel(); // إيقاف أي صوت سابق
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "it-IT";
    utterance.rate = rate;
    utterance.pitch = 1.0;

    if (this.italianVoice) {
      utterance.voice = this.italianVoice;
    }

    this.speechSynthesis.speak(utterance);
  }

  /**
   * تشغيل نغمة صوتية سريعة للتفاعل (UI Feedback Tone)
   * @param {'click'|'correct'|'error'|'flip'} type 
   */
  playFeedbackTone(type = "click") {
    if (this.isMuted) return;
    this.ensureAudioContext();
    if (!this.audioCtx) return;

    try {
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.connect(gain);
      gain.connect(this.audioCtx.destination);

      const now = this.audioCtx.currentTime;

      if (type === "correct") {
        // نغمة نجاح صاعدة لطيفة
        osc.frequency.setValueAtTime(523.25, now); // C5
        osc.frequency.exponentialRampToValueAtTime(659.25, now + 0.12); // E5
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.25);
        osc.start(now);
        osc.stop(now + 0.25);
      } else if (type === "error") {
        // نغمة تنبيه منخفضة
        osc.frequency.setValueAtTime(220, now); // A3
        osc.frequency.linearRampToValueAtTime(164.81, now + 0.15); // E3
        gain.gain.setValueAtTime(0.18, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.25);
        osc.start(now);
        osc.stop(now + 0.25);
      } else if (type === "flip") {
        // نغمة احتكاك ناعمة لقلب الكارت
        osc.type = "sine";
        osc.frequency.setValueAtTime(320, now);
        osc.frequency.exponentialRampToValueAtTime(480, now + 0.08);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.1);
        osc.start(now);
        osc.stop(now + 0.1);
      } else {
        // نغمة نقر خفيفة (Click)
        osc.type = "triangle";
        osc.frequency.setValueAtTime(600, now);
        gain.gain.setValueAtTime(0.05, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.04);
        osc.start(now);
        osc.stop(now + 0.04);
      }
    } catch (e) {
      // تجاهل إذا كانت قيود المتصفح مفعلة
    }
  }

  /**
   * تبديل كتم الصوت
   */
  toggleMute() {
    this.isMuted = !this.isMuted;
    if (this.isMuted && this.speechSynthesis) {
      this.speechSynthesis.cancel();
    }
    return this.isMuted;
  }
}

// تصدير المحرك
if (typeof window !== "undefined") {
  window.PatenteAudioEngine = PatenteAudioEngine;
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = PatenteAudioEngine;
}
