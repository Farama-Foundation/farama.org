(() => {
  const now = new Date();
  if (now.getUTCMonth() !== 11) return;

  const docsContent = document.querySelector(".main-container, .main > .content");
  const siteNavigation = document.getElementById("nav");
  if (!docsContent && !siteNavigation) return;

  document.getElementById("farama-donate-banner")?.remove();

  const dismissalKey = `farama-fundraiser-${now.getUTCFullYear()}-dismissed`;
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
        <p class="farama-fundraiser__label">Farama’s annual December fundraiser</p>
        <h2 id="farama-fundraiser-heading">Help keep Farama’s tools free and open</h2>
        <p>If Gymnasium, PettingZoo, or another Farama library has helped you learn, teach, or build, please consider giving this December. Your donation supports the developers who maintain these tools.</p>
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
