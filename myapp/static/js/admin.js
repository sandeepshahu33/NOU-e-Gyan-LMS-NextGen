/**
 * NOU E-GYAN Portal - Admin Dashboard Core JavaScript
 * High performance, zero unnecessary overhead, bulletproof navigation
 */
(function () {
  'use strict';

  var sidebar = document.getElementById('sidebar');
  var backdrop = document.getElementById('backdrop');
  var menuToggle = document.getElementById('menuToggle');
  var sidebarCloseBtn = document.getElementById('sidebarCloseBtn');
  var mainWrapper = document.getElementById('mainWrapper');

  // Toggle drawer / sidebar (works seamlessly on mobile and desktop)
  function toggleSidebar(open) {
    if (!sidebar) return;
    var isMobile = window.innerWidth < 992;

    if (isMobile) {
      if (typeof open === 'boolean') {
        sidebar.classList.toggle('open', open);
      } else {
        sidebar.classList.toggle('open');
      }
      if (backdrop) {
        backdrop.classList.toggle('show', sidebar.classList.contains('open'));
      }
    } else {
      // Desktop drawer collapse / expand
      if (typeof open === 'boolean') {
        sidebar.classList.toggle('collapsed', !open);
        if (mainWrapper) mainWrapper.classList.toggle('sidebar-collapsed', !open);
      } else {
        sidebar.classList.toggle('collapsed');
        if (mainWrapper) mainWrapper.classList.toggle('sidebar-collapsed');
      }
    }
  }

  if (menuToggle) {
    menuToggle.addEventListener('click', function (e) {
      e.stopPropagation();
      toggleSidebar();
    });
  }

  if (sidebarCloseBtn) {
    sidebarCloseBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      toggleSidebar(false);
    });
  }

  if (backdrop) {
    backdrop.addEventListener('click', function () {
      toggleSidebar(false);
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && sidebar) {
      if (sidebar.classList.contains('open') || !sidebar.classList.contains('collapsed')) {
        toggleSidebar(false);
      }
    }
  });

  // Safe navigation handling - NEVER preventDefault on actual URLs!
  document.querySelectorAll('.menu-link').forEach(function (link) {
    var href = link.getAttribute('href');
    
    if (!href || href === '#' || href.startsWith('javascript:')) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        var title = link.getAttribute('data-title') || link.innerText.trim();
        if (window.showPremiumToast) {
          window.showPremiumToast('The "' + title + '" module is scheduled for the next deployment phase.', 'info', 'Module in Progress');
        }
        if (window.innerWidth < 992) toggleSidebar(false);
      });
    } else {
      link.addEventListener('click', function () {
        if (window.innerWidth < 992) toggleSidebar(false);
      });
    }
  });

  // Synchronize active menu item with current URL
  function syncActiveMenu() {
    var path = window.location.pathname;
    var links = document.querySelectorAll('.menu-link');
    var matched = false;

    links.forEach(function (link) {
      var href = link.getAttribute('href');
      if (href && href !== '#' && !href.startsWith('javascript:')) {
        if (path === href || (href !== '/' && path.startsWith(href))) {
          link.classList.add('active');
          link.setAttribute('aria-current', 'page');
          matched = true;
        } else {
          link.classList.remove('active');
          link.removeAttribute('aria-current');
        }
      }
    });

    if (!matched && (path.includes('admindash') || path === '/admin/')) {
      var dashLink = document.querySelector('.menu-link[data-title="Dashboard"]');
      if (dashLink) {
        dashLink.classList.add('active');
        dashLink.setAttribute('aria-current', 'page');
      }
    }
  }
  syncActiveMenu();

  // Ctrl/Cmd + K quick search focus
  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      var searchInput = document.getElementById('search') || document.querySelector('input[type="search"]');
      if (searchInput) {
        e.preventDefault();
        searchInput.focus();
      }
    }
  });

  // ==========================================================================
  // ULTRA-PREMIUM TOAST NOTIFICATION ENGINE (ADMIN)
  // ==========================================================================
  function closePremiumToast(toastEl) {
    if (!toastEl || toastEl.classList.contains('toast-exit')) return;
    toastEl.classList.add('toast-exit');
    setTimeout(function () {
      if (toastEl && toastEl.parentNode) {
        toastEl.remove();
      }
    }, 330);
  }
  window.closePremiumToast = closePremiumToast;

  function bindToastTimer(toastEl) {
    if (!toastEl || toastEl.getAttribute('data-initialized') === 'true') return;
    toastEl.setAttribute('data-initialized', 'true');

    var duration = 4000;
    var remainingTime = duration;
    var startTime = Date.now();
    var timerId = null;

    function startTimer() {
      startTime = Date.now();
      timerId = setTimeout(function () {
        closePremiumToast(toastEl);
      }, remainingTime);
    }

    function pauseTimer() {
      clearTimeout(timerId);
      remainingTime -= (Date.now() - startTime);
      if (remainingTime < 250) remainingTime = 250;
      toastEl.classList.add('paused');
    }

    function resumeTimer() {
      toastEl.classList.remove('paused');
      startTimer();
    }

    toastEl.addEventListener('mouseenter', pauseTimer);
    toastEl.addEventListener('mouseleave', resumeTimer);

    startTimer();
  }
  window.bindToastTimer = bindToastTimer;

  function showPremiumToast(message, type, title) {
    var container = document.getElementById('premiumToastContainer');
    if (!container) {
      container = document.createElement('div');
      container.id = 'premiumToastContainer';
      container.className = 'premium-toast-container';
      document.body.appendChild(container);
    }

    var normalizedType = (type || 'info').toLowerCase();
    var iconClass = 'bi-info-circle-fill';
    var defaultTitle = 'Notification';

    if (normalizedType.includes('success')) {
      iconClass = 'bi-check-circle-fill text-success';
      defaultTitle = 'Success';
      normalizedType = 'success';
    } else if (normalizedType.includes('danger') || normalizedType.includes('error')) {
      iconClass = 'bi-exclamation-octagon-fill text-danger';
      defaultTitle = 'Alert';
      normalizedType = 'danger';
    } else if (normalizedType.includes('warning')) {
      iconClass = 'bi-exclamation-triangle-fill text-warning';
      defaultTitle = 'Warning';
      normalizedType = 'warning';
    } else {
      iconClass = 'bi-info-circle-fill text-warning';
      defaultTitle = 'Notice';
      normalizedType = 'info';
    }

    var toastEl = document.createElement('div');
    toastEl.className = 'premium-toast';
    toastEl.setAttribute('data-toast-type', normalizedType);
    toastEl.setAttribute('role', 'alert');

    toastEl.innerHTML = `
      <div class="toast-accent-line"></div>
      <div class="toast-icon-wrap">
        <i class="bi ${iconClass}"></i>
      </div>
      <div class="toast-content">
        <div class="toast-header-row">
          <span class="toast-title">${title || defaultTitle}</span>
          <span class="toast-time">just now</span>
        </div>
        <div class="toast-message">${message}</div>
      </div>
      <button type="button" class="toast-close-btn" aria-label="Close notification" onclick="closePremiumToast(this.closest('.premium-toast'))">
        <i class="bi bi-x-lg"></i>
      </button>
      <div class="toast-progress-track">
        <div class="toast-progress-bar"></div>
      </div>
    `;

    container.appendChild(toastEl);
    bindToastTimer(toastEl);
    return toastEl;
  }
  window.showPremiumToast = showPremiumToast;

  // Initialize existing toasts from Django backend on load
  function initDjangoToasts() {
    var toasts = document.querySelectorAll('.premium-toast:not([data-initialized="true"])');
    toasts.forEach(function (el) {
      bindToastTimer(el);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDjangoToasts);
  } else {
    initDjangoToasts();
  }
})();
