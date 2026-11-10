(() => {
  const campaignStart = Date.UTC(2026, 11, 1);
  const campaignEnd = Date.UTC(2027, 0, 1);
  const now = Date.now();
  if (now < campaignStart || now >= campaignEnd) return;

  const docsContent = document.querySelector(".main-container, .main > .content");
  const siteNavigation = document.getElementById("nav");
  if (!docsContent && !siteNavigation) return;

  document.getElementById("farama-donate-banner")?.remove();

  const dismissalKey = "farama-fundraiser-2026-dismissed";
  try {
    if (localStorage.getItem(dismissalKey)) return;
  } catch {
    // Storage may be disabled. Dismissal still works on the current page.
  }

  if (document.getElementById("farama-december-fundraiser")) return;

  const banner = document.createElement("aside");
  banner.id = "farama-december-fundraiser";
  banner.setAttribute("aria-labelledby", "farama-fundraiser-heading");
  banner.hidden = true;
  banner.innerHTML = `
    <div class="farama-fundraiser__inner">
      <div class="farama-fundraiser__copy">
        <h2 id="farama-fundraiser-heading">Help keep reinforcement learning tools open</h2>
        <p>Donate to the Farama Foundation this December to support the developers who maintain Gymnasium, PettingZoo, and our other open-source libraries.</p>
      </div>
      <a class="farama-fundraiser__donate" href="https://farama.org/donations">Donate to Farama</a>
      <button class="farama-fundraiser__close" type="button" aria-label="Dismiss fundraising banner">×</button>
    </div>
  `;

  const close = banner.querySelector("button");
  close.addEventListener("click", () => {
    try {
      localStorage.setItem(dismissalKey, "true");
    } catch {
      // The banner can still be dismissed when storage is unavailable.
    }
    const restoreFocus = document.activeElement === close;
    banner.remove();
    if (restoreFocus) {
      document.querySelector(".farama-header a, #nav a")?.focus();
    }
  });

  const stylesheet = document.createElement("link");
  stylesheet.rel = "stylesheet";
  stylesheet.href = new URL("december-fundraiser.css", document.currentScript.src).href;
  stylesheet.onload = () => {
    banner.hidden = false;
  };
  document.head.append(stylesheet);

  if (siteNavigation) {
    siteNavigation.before(banner);
  } else {
    docsContent.prepend(banner);
  }
})();
