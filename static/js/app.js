(function () {
    "use strict";
  
    const API_BASE = "";
    const THEME_KEY = "convo-clarity-theme";
    const HISTORY_KEY = "convo-clarity-history";
    const MAX_HISTORY = 40;
  
    const examples = [
      {
        title: "Daily stand‑up recap",
        text:
          "PM: Quick stand-up: we need to lock features by Wednesday.\n" +
          "Dev: Signup bug is fixed, working on profile page.\n" +
          "Designer: Updating empty state illustrations.\n" +
          "PM: Launch still Friday, only critical bugs after Wednesday.",
      },
      {
        title: "Support chat",
        text:
          "User: My password reset link expired again.\n" +
          "Agent: I’m sorry about that. When did you click it?\n" +
          "User: About 3 hours after I received it.\n" +
          "Agent: The link is valid for 2 hours. I’ll send a new link and extend it to 24 hours. " +
          "Please try again and reply here if it fails.",
      },
      {
        title: "Long WhatsApp thread",
        text:
          "A: We should plan the trip this weekend.\n" +
          "B: I can do Saturday afternoon only.\n" +
          "C: Sunday is better for me, maybe brunch.\n" +
          "A: Let’s do Sunday 11am, meet at the station, I’ll book the table.\n" +
          "B: Works for me.\n" +
          "C: Perfect, see you then!",
      },
      {
        title: "Meeting notes",
        text:
          "Manager: We need to reduce support response time.\n" +
          "Lead: Current average is 18 hours.\n" +
          "Manager: Goal is 6 hours by next quarter.\n" +
          "Lead: We'll add one more agent to the early shift and create email templates.\n" +
          "Manager: Review progress in two weeks.",
      },
    ];
  
    const $ = (id) => document.getElementById(id);
  
    function setTheme(theme) {
      const next = theme === "light" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next === "light" ? "light" : "dark");
      localStorage.setItem(THEME_KEY, next);
      const btn = $("themeToggle");
    //   if (btn) btn.textContent = next === "light" ? "Light" : "Dark";
    if (btn) btn.textContent = next === "light" ? "Dark mode" : "Light mode";
    }
  
    function initTheme() {
      const stored = localStorage.getItem(THEME_KEY);
      setTheme(stored || "light");
      const btn = $("themeToggle");
      if (btn) {
        btn.addEventListener("click", () => {
          const current = document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
          setTheme(current === "light" ? "dark" : "light");
        });
      }
    }
  
    async function checkHealth() {
      const statusEl = $("apiStatus");
      if (!statusEl) return;
      try {
        const res = await fetch(API_BASE + "/api/health");
        if (!res.ok) throw new Error();
        statusEl.classList.add("status-online");
        statusEl.classList.remove("status-offline");
        const text = statusEl.querySelector(".status-text");
        if (text) text.textContent = "Live now";
      } catch {
        statusEl.classList.add("status-offline");
        statusEl.classList.remove("status-online");
        const text = statusEl.querySelector(".status-text");
        if (text) text.textContent = "Offline — check server";
      }
    }
  
    function updateInputCounts() {
      const ta = $("inputText");
      const wordsEl = $("inputWordCount");
      const charsEl = $("inputCharCount");
      if (!ta || !wordsEl || !charsEl) return;
      const text = ta.value || "";
      const words = text.trim() ? text.trim().split(/\s+/).length : 0;
      wordsEl.textContent = `${words} words`;
      charsEl.textContent = `${text.length} characters`;
    }
  
    function setSummarizeLoading(isLoading) {
      const btn = $("summarizeBtn");
      if (!btn) return;
      btn.classList.toggle("loading", isLoading);
      btn.disabled = isLoading;
    }
  
    function showError(msg) {
      const box = $("errorBox");
      const wrap = $("summaryWrap");
      if (box) {
        box.textContent = msg;
        box.hidden = false;
      }
      if (wrap) wrap.hidden = true;
    }
  
    function hideError() {
      const box = $("errorBox");
      if (box) box.hidden = true;
    }
  
    async function doSummarize() {
      const ta = $("inputText");
      if (!ta) return;
      const text = (ta.value || "").trim();
      if (!text) {
        showError("Please paste some text first.");
        return;
      }
      setSummarizeLoading(true);
      hideError();
      try {
        const res = await fetch(API_BASE + "/api/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text }),
        });
        if (!res.ok) {
          const err = await res.json().catch(() => ({}));
          throw new Error(err.detail || "Something went wrong. Try again.");
        }
        const data = await res.json();
        const summary = data.summary || "";
        const inputLen = data.input_length || text.split(/\s+/).length;
        const summaryLen = data.summary_length || (summary ? summary.split(/\s+/).length : 0);
        renderSummary(summary, inputLen, summaryLen);
        addToHistory(text, summary);
      } catch (err) {
        showError(err.message || "Could not summarize this text.");
      } finally {
        setSummarizeLoading(false);
      }
    }
  
    function renderSummary(summary, inputLen, summaryLen) {
      const wrap = $("summaryWrap");
      const textEl = $("summaryText");
      const stats = $("outputStats");
      if (!wrap || !textEl || !stats) return;
      textEl.textContent = summary;
      stats.textContent = `${summaryLen} words (input had ${inputLen} words)`;
      wrap.hidden = false;
    }
  
    function clearInput() {
      const ta = $("inputText");
      if (!ta) return;
      ta.value = "";
      updateInputCounts();
      hideError();
      const wrap = $("summaryWrap");
      if (wrap) wrap.hidden = true;
    }
  
    function copySummary() {
      const textEl = $("summaryText");
      if (!textEl || !textEl.textContent) return;
      navigator.clipboard.writeText(textEl.textContent).then(() => {
        const btn = $("copyBtn");
        if (!btn) return;
        const original = btn.textContent;
        btn.textContent = "Copied!";
        setTimeout(() => (btn.textContent = original), 1500);
      });
    }
  
    function downloadSummary() {
      const textEl = $("summaryText");
      if (!textEl || !textEl.textContent) return;
      const blob = new Blob([textEl.textContent], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "convo-clarity-summary.txt";
      a.click();
      URL.revokeObjectURL(url);
    }
  
    function loadHistory() {
      try {
        const raw = localStorage.getItem(HISTORY_KEY);
        return raw ? JSON.parse(raw) : [];
      } catch {
        return [];
      }
    }
  
    function saveHistory(list) {
      try {
        localStorage.setItem(HISTORY_KEY, JSON.stringify(list.slice(0, MAX_HISTORY)));
      } catch {
        // ignore
      }
    }
  
    function addToHistory(input, summary) {
      const list = loadHistory();
      list.unshift({
        input,
        summary,
        at: new Date().toISOString(),
      });
      saveHistory(list);
    }
  
    function renderExamples() {
      const grid = $("examplesGrid");
      if (!grid) return;
      grid.innerHTML = "";
      examples.forEach((ex) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "example-card";
        const preview =
          ex.text.length > 120 ? ex.text.slice(0, 120) + "…" : ex.text;
        btn.innerHTML =
          `<div class="example-title">${escapeHtml(ex.title)}</div>` +
          `<div class="example-preview">${escapeHtml(preview)}</div>`;
        btn.addEventListener("click", () => {
          const ta = $("inputText");
          if (!ta) return;
          ta.value = ex.text;
          updateInputCounts();
          hideError();
          const wrap = $("summaryWrap");
          if (wrap) wrap.hidden = true;
        });
        grid.appendChild(btn);
      });
    }
  
    function escapeHtml(str) {
      const div = document.createElement("div");
      div.textContent = String(str);
      return div.innerHTML;
    }
  
    function setupScrollReveal() {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("visible");
              observer.unobserve(entry.target);
            }
          });
        },
        {
          threshold: 0.1,
          rootMargin: "0px 0px -50px 0px",
        }
      );
      document.querySelectorAll(".reveal").forEach((el) => {
        observer.observe(el);
      });
    }
  
    function setupNav() {
      const burger = $("navBurger");
      const links = $("navLinks");
      if (!burger || !links) return;
      burger.addEventListener("click", () => {
        links.classList.toggle("open");
      });
      links.querySelectorAll("a").forEach((a) => {
        a.addEventListener("click", () => links.classList.remove("open"));
      });
    }
  
    function initEvents() {
      const ta = $("inputText");
      if (ta) {
        ta.addEventListener("input", updateInputCounts);
        ta.addEventListener("keydown", (e) => {
          if (e.ctrlKey && e.key === "Enter") {
            e.preventDefault();
            doSummarize();
          }
        });
      }
      const sumBtn = $("summarizeBtn");
      if (sumBtn) sumBtn.addEventListener("click", doSummarize);
      const clearBtn = $("clearBtn");
      if (clearBtn) clearBtn.addEventListener("click", clearInput);
      const copyBtn = $("copyBtn");
      if (copyBtn) copyBtn.addEventListener("click", copySummary);
      const dlBtn = $("downloadBtn");
      if (dlBtn) dlBtn.addEventListener("click", downloadSummary);
    }
  
    function init() {
      initTheme();
      updateInputCounts();
      renderExamples();
      setupScrollReveal();
      setupNav();
      initEvents();
      checkHealth();
      setInterval(checkHealth, 30000);
    }
  
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", init);
    } else {
      init();
    }
  })();