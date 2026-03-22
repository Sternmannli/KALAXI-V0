/**
 * threshold-client.js — KALAXI Threshold Client v1.0
 * The Living Bridge (frontend). Connects kalam.ch to the Witness Engine API.
 *
 * This client handles:
 *   - Donor intake ritual (4-step ceremony)
 *   - Real-time WebSocket threshold interaction
 *   - Canon fragment display (proverbs, narratives, treasures)
 *   - Dignity visualization (A × L × M)
 *   - Breath pulse animation
 *   - Witness certificate display
 *
 * Dependencies: None. Vanilla JS. No frameworks.
 *
 * Usage:
 *   <script src="/threshold-client.js"></script>
 *   <script>
 *     const kalaxi = new KalaxiThreshold({ apiUrl: 'https://api.kalam.ch' });
 *     kalaxi.mount('#threshold-container');
 *   </script>
 *
 * [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
 */

(function (root) {
  'use strict';

  // ═══════════════════════════════════════════════════
  // CONFIGURATION
  // ═══════════════════════════════════════════════════

  const DEFAULT_CONFIG = {
    apiUrl: '',  // Set to API server URL (e.g. 'http://localhost:8080')
    wsUrl: '',   // Auto-derived from apiUrl if empty
    breathInterval: 10000,  // Pulse check every 10 seconds
    dignityDelay: 300,      // ms delay for dignity-paced responses
    maxInputLength: 5000,
  };

  // ═══════════════════════════════════════════════════
  // KALAXI THRESHOLD — Main Class
  // ═══════════════════════════════════════════════════

  class KalaxiThreshold {
    constructor(config) {
      this.config = Object.assign({}, DEFAULT_CONFIG, config || {});
      if (!this.config.wsUrl && this.config.apiUrl) {
        this.config.wsUrl = this.config.apiUrl.replace(/^http/, 'ws') + '/ws';
      }
      this.ws = null;
      this.sessionId = null;
      this.stage = 'idle';  // idle, greeting, consent, voice, receipt, complete, threshold
      this.container = null;
      this.breathTimer = null;
      this.witnessCount = 0;
    }

    // ── MOUNT ──

    mount(selector) {
      this.container = typeof selector === 'string'
        ? document.querySelector(selector)
        : selector;

      if (!this.container) {
        console.error('[KALAXI] Container not found:', selector);
        return;
      }

      this._render();
      this._bindEvents();
    }

    // ── RENDER ──

    _render() {
      this.container.innerHTML = `
        <div class="kalaxi-threshold" role="main" aria-label="KALAXI Threshold">
          <!-- Status bar -->
          <div class="kalaxi-status" id="kalaxi-status">
            <span class="kalaxi-breath-dot" id="kalaxi-breath-dot"></span>
            <span id="kalaxi-status-text">The door is open.</span>
          </div>

          <!-- Dignity display -->
          <div class="kalaxi-dignity" id="kalaxi-dignity" style="display:none;">
            <div class="kalaxi-dignity-bar">
              <div class="kalaxi-dignity-component" id="kalaxi-A">
                <span class="kalaxi-dignity-label">A</span>
                <div class="kalaxi-dignity-fill" id="kalaxi-A-fill"></div>
                <span class="kalaxi-dignity-value" id="kalaxi-A-value">—</span>
              </div>
              <div class="kalaxi-dignity-component" id="kalaxi-L">
                <span class="kalaxi-dignity-label">L</span>
                <div class="kalaxi-dignity-fill" id="kalaxi-L-fill"></div>
                <span class="kalaxi-dignity-value" id="kalaxi-L-value">—</span>
              </div>
              <div class="kalaxi-dignity-component" id="kalaxi-M">
                <span class="kalaxi-dignity-label">M</span>
                <div class="kalaxi-dignity-fill" id="kalaxi-M-fill"></div>
                <span class="kalaxi-dignity-value" id="kalaxi-M-value">—</span>
              </div>
            </div>
            <div class="kalaxi-dignity-total" id="kalaxi-D-value">D = —</div>
          </div>

          <!-- Response area -->
          <div class="kalaxi-response" id="kalaxi-response" aria-live="polite">
            <p class="kalaxi-voice" id="kalaxi-voice-text"></p>
            <p class="kalaxi-source" id="kalaxi-voice-source"></p>
          </div>

          <!-- Input area -->
          <div class="kalaxi-input-area" id="kalaxi-input-area">
            <textarea
              id="kalaxi-input"
              class="kalaxi-input"
              placeholder="qul"
              rows="2"
              maxlength="5000"
              aria-label="Speak to the system"
            ></textarea>
            <button id="kalaxi-send" class="kalaxi-send" aria-label="Send">
              ●
            </button>
          </div>

          <!-- Action buttons (for intake ritual) -->
          <div class="kalaxi-actions" id="kalaxi-actions" style="display:none;">
            <button id="kalaxi-consent-yes" class="kalaxi-btn">I consent</button>
            <button id="kalaxi-consent-no" class="kalaxi-btn kalaxi-btn-secondary">I withdraw</button>
          </div>

          <!-- Canon display -->
          <div class="kalaxi-canon" id="kalaxi-canon" style="display:none;">
            <p class="kalaxi-canon-text" id="kalaxi-canon-text"></p>
            <p class="kalaxi-canon-source" id="kalaxi-canon-source"></p>
          </div>

          <!-- Witness mark counter -->
          <div class="kalaxi-witness-mark" id="kalaxi-witness-mark">
            <span id="kalaxi-witness-count">0</span> witness marks
          </div>
        </div>

        <style>
          .kalaxi-threshold {
            font-family: 'Courier New', Courier, monospace;
            max-width: 640px;
            margin: 0 auto;
            padding: 2rem 1rem;
            color: #1a1a1a;
            line-height: 1.6;
          }

          .kalaxi-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
            font-size: 0.85rem;
            color: #666;
          }

          .kalaxi-breath-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #2d5a27;
            animation: kalaxi-breathe 4s ease-in-out infinite;
          }

          @keyframes kalaxi-breathe {
            0%, 100% { opacity: 0.3; transform: scale(0.8); }
            50% { opacity: 1; transform: scale(1.2); }
          }

          .kalaxi-dignity {
            margin-bottom: 1.5rem;
            padding: 1rem;
            background: #fafafa;
            border-left: 3px solid #1a1a1a;
          }

          .kalaxi-dignity-bar {
            display: flex;
            gap: 1rem;
            margin-bottom: 0.5rem;
          }

          .kalaxi-dignity-component {
            flex: 1;
            text-align: center;
          }

          .kalaxi-dignity-label {
            font-size: 0.75rem;
            font-weight: bold;
            display: block;
            margin-bottom: 0.25rem;
          }

          .kalaxi-dignity-fill {
            height: 4px;
            background: #2d5a27;
            transition: width 0.8s ease;
            width: 0%;
          }

          .kalaxi-dignity-value {
            font-size: 0.75rem;
            color: #666;
          }

          .kalaxi-dignity-total {
            text-align: center;
            font-weight: bold;
            font-size: 1.1rem;
            margin-top: 0.5rem;
          }

          .kalaxi-response {
            min-height: 80px;
            margin-bottom: 1.5rem;
            padding: 1rem 0;
          }

          .kalaxi-voice {
            font-size: 1.05rem;
            line-height: 1.7;
            margin: 0 0 0.5rem 0;
          }

          .kalaxi-source {
            font-size: 0.75rem;
            color: #999;
            margin: 0;
          }

          .kalaxi-input-area {
            display: flex;
            gap: 0.5rem;
            align-items: flex-end;
            margin-bottom: 1rem;
          }

          .kalaxi-input {
            flex: 1;
            font-family: inherit;
            font-size: 1rem;
            padding: 0.75rem;
            border: 1px solid #ccc;
            border-radius: 0;
            resize: none;
            background: #fff;
            color: #1a1a1a;
            outline: none;
            transition: border-color 0.3s;
          }

          .kalaxi-input:focus {
            border-color: #1a1a1a;
          }

          .kalaxi-input::placeholder {
            color: #ccc;
            font-style: italic;
          }

          .kalaxi-send {
            width: 44px;
            height: 44px;
            border: 1px solid #1a1a1a;
            background: #1a1a1a;
            color: #fff;
            font-size: 1rem;
            cursor: pointer;
            border-radius: 0;
            transition: opacity 0.3s;
          }

          .kalaxi-send:hover {
            opacity: 0.8;
          }

          .kalaxi-actions {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
          }

          .kalaxi-btn {
            padding: 0.5rem 1.5rem;
            font-family: inherit;
            font-size: 0.9rem;
            border: 1px solid #1a1a1a;
            background: #1a1a1a;
            color: #fff;
            cursor: pointer;
          }

          .kalaxi-btn-secondary {
            background: #fff;
            color: #1a1a1a;
          }

          .kalaxi-canon {
            padding: 1rem;
            background: #f5f0e8;
            border-left: 3px solid #8b7355;
            margin-bottom: 1rem;
          }

          .kalaxi-canon-text {
            font-size: 0.95rem;
            font-style: italic;
            margin: 0 0 0.25rem 0;
          }

          .kalaxi-canon-source {
            font-size: 0.7rem;
            color: #8b7355;
            margin: 0;
          }

          .kalaxi-witness-mark {
            font-size: 0.75rem;
            color: #999;
            text-align: center;
            margin-top: 2rem;
          }

          /* Dignity failure state */
          .kalaxi-threshold.dignity-halt .kalaxi-dignity {
            border-left-color: #8b0000;
          }

          .kalaxi-threshold.dignity-halt .kalaxi-dignity-fill {
            background: #8b0000;
          }
        </style>
      `;
    }

    // ── BIND EVENTS ──

    _bindEvents() {
      const input = this.container.querySelector('#kalaxi-input');
      const sendBtn = this.container.querySelector('#kalaxi-send');
      const consentYes = this.container.querySelector('#kalaxi-consent-yes');
      const consentNo = this.container.querySelector('#kalaxi-consent-no');

      // Send on button click
      sendBtn.addEventListener('click', () => this._handleSend());

      // Send on Enter (Shift+Enter for newline)
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this._handleSend();
        }
      });

      // Consent buttons
      consentYes.addEventListener('click', () => this._handleConsent(true));
      consentNo.addEventListener('click', () => this._handleConsent(false));
    }

    // ── HANDLE SEND ──

    async _handleSend() {
      const input = this.container.querySelector('#kalaxi-input');
      const text = input.value.trim();
      if (!text) return;

      input.value = '';
      input.disabled = true;

      try {
        if (this.stage === 'idle') {
          // First message — begin intake
          await this._beginIntake(text);
        } else if (this.stage === 'voice') {
          // Donor's first voice during intake
          await this._submitVoice(text);
        } else if (this.stage === 'threshold' || this.stage === 'complete') {
          // Ongoing interaction — witness
          await this._witness(text);
        }
      } catch (err) {
        this._showVoice('The system encountered difficulty. Please try again.', 'error');
        console.error('[KALAXI]', err);
      }

      input.disabled = false;
      input.focus();
    }

    // ── INTAKE RITUAL ──

    async _beginIntake(firstText) {
      this._setStatus('Opening the door...');

      try {
        const resp = await this._api('POST', '/intake/begin');
        this.sessionId = resp.session_id;
        this.stage = 'greeting';

        // Show greeting and consent text
        this._showVoice(resp.greeting, 'system');
        this._setStatus('The system awaits your decision.');

        // Show consent buttons
        this.container.querySelector('#kalaxi-actions').style.display = 'flex';
        this.container.querySelector('#kalaxi-input-area').style.display = 'none';

        // Store the first text for after consent
        this._pendingVoice = firstText;
      } catch (err) {
        // If intake fails, go directly to witness mode
        this.stage = 'threshold';
        await this._witness(firstText);
      }
    }

    async _handleConsent(agreed) {
      this.container.querySelector('#kalaxi-actions').style.display = 'none';
      this.container.querySelector('#kalaxi-input-area').style.display = 'flex';

      if (!agreed) {
        this._showVoice('Your decision is respected. The door remains open.', 'system');
        this.stage = 'idle';
        this.sessionId = null;
        this._setStatus('The door is open.');
        return;
      }

      try {
        await this._api('POST', '/intake/consent', {
          session_id: this.sessionId,
          agreed: true,
        });
        this.stage = 'voice';
        this._showVoice('Consent recorded. Now, speak — the system listens.', 'system');
        this._setStatus('The system listens.');

        // If we have a pending voice, submit it now
        if (this._pendingVoice) {
          await this._submitVoice(this._pendingVoice);
          this._pendingVoice = null;
        }
      } catch (err) {
        this._showVoice('The consent step encountered difficulty.', 'error');
        this.stage = 'threshold';
      }
    }

    async _submitVoice(text) {
      this._setStatus('The system witnesses...');

      try {
        const resp = await this._api('POST', '/intake/voice', {
          session_id: this.sessionId,
          voice: text,
        });

        if (resp.sealed_gate === false) {
          this._showVoice('The sealed door activated. Please rephrase.', 'system');
          return;
        }

        // Show dignity score
        this._showDignity({
          A: resp.dignity_score || 0.8,
          L: resp.dignity_score || 0.8,
          M: resp.dignity_score || 0.8,
          D: resp.dignity_score || 0.8,
        });

        // Complete intake
        await this._completeIntake();
      } catch (err) {
        // Fallback to witness mode
        this.stage = 'threshold';
        await this._witness(text);
      }
    }

    async _completeIntake() {
      try {
        const resp = await this._api('POST', '/intake/receipt', {
          session_id: this.sessionId,
        });
        this._showVoice(resp.receipt_text || resp.message, 'system');
        this.stage = 'complete';
        this._setStatus('Intake complete. The threshold is open.');

        // Connect WebSocket for ongoing interaction
        this._connectWS();
      } catch (err) {
        this.stage = 'threshold';
        this._setStatus('The threshold is open.');
      }
    }

    // ── WITNESS — The Core Act ──

    async _witness(text) {
      this._setStatus('Witnessing...');

      try {
        const resp = await this._api('POST', '/witness', { text: text });

        // Show dignity
        this._showDignity(resp.dignity_components);

        // Show voice response
        this._showVoice(resp.voice_text, resp.voice_sources.join(', '));

        // Update witness count
        this.witnessCount++;
        const counter = this.container.querySelector('#kalaxi-witness-count');
        if (counter) counter.textContent = this.witnessCount;

        // Dignity halt state
        if (!resp.dignity_passed) {
          this.container.querySelector('.kalaxi-threshold').classList.add('dignity-halt');
          this._setStatus('The system halted. Dignity could not be maintained.');
        } else {
          this.container.querySelector('.kalaxi-threshold').classList.remove('dignity-halt');
          this._setStatus('Witnessed.');
        }

        this.stage = 'threshold';
      } catch (err) {
        // Try WebSocket if HTTP fails
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(JSON.stringify({ type: 'voice', text: text }));
        } else {
          this._showVoice('The system could not witness. The door stays open.', 'error');
        }
        this._setStatus('The door is open.');
      }
    }

    // ── WEBSOCKET ──

    _connectWS() {
      if (!this.config.wsUrl) return;

      try {
        this.ws = new WebSocket(this.config.wsUrl);

        this.ws.onopen = () => {
          this._setStatus('Connected. The threshold breathes.');
          this._startBreath();
        };

        this.ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this._handleWSMessage(data);
          } catch (e) {
            console.error('[KALAXI] WS parse error:', e);
          }
        };

        this.ws.onclose = () => {
          this._setStatus('Connection closed. The door remains open.');
          this._stopBreath();
        };

        this.ws.onerror = () => {
          console.warn('[KALAXI] WebSocket error — falling back to HTTP.');
        };
      } catch (err) {
        console.warn('[KALAXI] WebSocket not available — HTTP mode.');
      }
    }

    _handleWSMessage(data) {
      switch (data.type) {
        case 'greeting':
          // Already shown during intake
          break;

        case 'witness':
          this._showVoice(data.voice_text, data.voice_sources?.join(', ') || '');
          if (data.dignity) {
            this._showDignity(data.dignity);
          }
          this.witnessCount++;
          const counter = this.container.querySelector('#kalaxi-witness-count');
          if (counter) counter.textContent = this.witnessCount;
          break;

        case 'pulse':
          // Update breath indicator
          this._setStatus(`Breathing. Cycle ${data.cycle}. ${data.witnesses || 0} witnesses.`);
          break;

        case 'fragment':
          this._showCanon(data.text, `${data.source}${data.book ? ' · ' + data.book : ''}`);
          break;

        case 'silence':
          this._showVoice(data.text, 'silence');
          break;

        case 'farewell':
          this._showVoice(data.text, 'system');
          break;
      }
    }

    _startBreath() {
      this.breathTimer = setInterval(() => {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(JSON.stringify({ type: 'breath' }));
        }
      }, this.config.breathInterval);
    }

    _stopBreath() {
      if (this.breathTimer) {
        clearInterval(this.breathTimer);
        this.breathTimer = null;
      }
    }

    // ── DISPLAY HELPERS ──

    _showVoice(text, source) {
      const voiceEl = this.container.querySelector('#kalaxi-voice-text');
      const sourceEl = this.container.querySelector('#kalaxi-voice-source');
      if (voiceEl) voiceEl.textContent = text;
      if (sourceEl) sourceEl.textContent = source || '';
    }

    _showDignity(components) {
      const dignityEl = this.container.querySelector('#kalaxi-dignity');
      if (!dignityEl) return;

      dignityEl.style.display = 'block';

      const A = components.A || 0;
      const L = components.L || 0;
      const M = components.M || 0;
      const D = components.D || (A * L * M);

      // Update fills
      const aFill = this.container.querySelector('#kalaxi-A-fill');
      const lFill = this.container.querySelector('#kalaxi-L-fill');
      const mFill = this.container.querySelector('#kalaxi-M-fill');

      if (aFill) aFill.style.width = (A * 100) + '%';
      if (lFill) lFill.style.width = (L * 100) + '%';
      if (mFill) mFill.style.width = (M * 100) + '%';

      // Update values
      const aVal = this.container.querySelector('#kalaxi-A-value');
      const lVal = this.container.querySelector('#kalaxi-L-value');
      const mVal = this.container.querySelector('#kalaxi-M-value');
      const dVal = this.container.querySelector('#kalaxi-D-value');

      if (aVal) aVal.textContent = A.toFixed(2);
      if (lVal) lVal.textContent = L.toFixed(2);
      if (mVal) mVal.textContent = M.toFixed(2);
      if (dVal) dVal.textContent = 'D = ' + D.toFixed(3);
    }

    _showCanon(text, source) {
      const canonEl = this.container.querySelector('#kalaxi-canon');
      const textEl = this.container.querySelector('#kalaxi-canon-text');
      const sourceEl = this.container.querySelector('#kalaxi-canon-source');

      if (canonEl) canonEl.style.display = 'block';
      if (textEl) textEl.textContent = text;
      if (sourceEl) sourceEl.textContent = source || '';
    }

    _setStatus(text) {
      const statusEl = this.container.querySelector('#kalaxi-status-text');
      if (statusEl) statusEl.textContent = text;
    }

    // ── API HELPER ──

    async _api(method, path, body) {
      const url = this.config.apiUrl + path;
      const options = {
        method: method,
        headers: { 'Content-Type': 'application/json' },
      };

      if (body) {
        options.body = JSON.stringify(body);
      }

      const resp = await fetch(url, options);

      if (!resp.ok) {
        const err = await resp.json().catch(() => ({ detail: resp.statusText }));
        throw new Error(err.detail || 'API request failed');
      }

      return resp.json();
    }

    // ── PUBLIC METHODS ──

    async fetchProverb(theme) {
      const params = theme ? `?theme=${encodeURIComponent(theme)}` : '';
      return this._api('GET', '/canon/proverb' + params);
    }

    async fetchNarrative(book) {
      const params = book ? `?book=${encodeURIComponent(book)}` : '';
      return this._api('GET', '/canon/narrative' + params);
    }

    async fetchBreath() {
      return this._api('GET', '/breath');
    }

    async checkDignity(text) {
      return this._api('POST', '/dignity/check', { text: text });
    }

    destroy() {
      this._stopBreath();
      if (this.ws) {
        this.ws.close();
        this.ws = null;
      }
      if (this.container) {
        this.container.innerHTML = '';
      }
    }
  }

  // ═══════════════════════════════════════════════════
  // EXPORT
  // ═══════════════════════════════════════════════════

  // UMD export
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = KalaxiThreshold;
  } else {
    root.KalaxiThreshold = KalaxiThreshold;
  }

})(typeof globalThis !== 'undefined' ? globalThis : typeof window !== 'undefined' ? window : this);
