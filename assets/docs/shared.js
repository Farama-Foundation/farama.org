// Shared header code for every Farama documentation site.
//
// Celshast (the docs theme) loads this file from farama.org on each page view,
// including on archived docs versions, so whatever changes here is live on all
// docs sites as soon as farama.org deploys. Nothing has to be released or
// rebuilt. Keep it dependency free and tolerant of old page markup: it runs on
// docs built years ago as well as on current ones.
(() => {
  if (window.faramaDocsShared) return;
  window.faramaDocsShared = true;

  // Resolved from this script's own URL so a local `jekyll serve` works too.
  const site = new URL(document.currentScript.src).origin;

  // ---- Farama project menu -------------------------------------------------

  const imageBase = `${site}/assets/images`;
  const foundationLinks = [
    { name: "About", website: `${site}/about` },
    { name: "Standards", website: `${site}/project_standards` },
    { name: "Donate", website: `${site}/donations` },
  ];

  function projectList(projects) {
    const list = document.createElement("ul");
    list.className = "farama-header-menu-list";

    for (const project of projects) {
      const item = document.createElement("li");
      const link = document.createElement("a");
      link.href = project.website ?? project.github;

      const logo = document.createElement("img");
      logo.src = imageBase + (project.image || "/farama_black.svg");
      logo.alt = "";
      logo.className = "farama-black-logo-invert";

      link.append(logo, project.name);
      item.append(link);
      list.append(item);
    }

    return list;
  }

  function section(title, className = "section") {
    const element = document.createElement("div");
    element.className = `farama-header-menu__${className}`;
    const heading = document.createElement("span");
    heading.className = `farama-header-menu__${className}-title`;
    heading.textContent = title;
    element.append(heading);
    return element;
  }

  function group(title, lists) {
    const element = section(title);
    const columns = document.createElement("div");
    columns.className = "farama-header-menu__subsections-container";
    columns.style.display = "flex";

    for (const [name, projects] of Object.entries(lists)) {
      const column = section(name, "subsection");
      column.append(projectList(projects));
      columns.append(column);
    }

    element.append(columns);
    return element;
  }

  function buildMenu(projects) {
    const core = [];
    const mature = [];
    const incubatingDocs = [];
    const incubatingRepos = [];
    for (const project of projects) {
      if (project.type === "core") {
        core.push(project);
      } else if (project.type === "mature") {
        if (project.website != null) mature.push(project);
      } else if (project.website != null) {
        incubatingDocs.push(project);
      } else {
        incubatingRepos.push(project);
      }
    }

    const coreSection = section("Core Projects");
    coreSection.append(projectList(core));
    const foundation = section("Foundation");
    foundation.append(projectList(foundationLinks));
    const stack = document.createElement("div");
    stack.style.cssText = "display: flex; flex-direction: column";
    stack.append(coreSection, foundation);

    return [
      stack,
      group("Mature Projects", { Documentation: mature }),
      group("Incubating Projects", { Documentation: incubatingDocs, Repositories: incubatingRepos }),
    ];
  }

  const menu = document.querySelector(".farama-header-menu__body");
  if (menu) {
    fetch(`${site}/api/projects.json`)
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
      })
      .then((projects) => {
        const sections = buildMenu(projects);
        const isCurrent = () =>
          menu.children.length === sections.length &&
          sections.every((element, i) => menu.children[i] === element);
        menu.replaceChildren(...sections);

        // Older docs builds fill the menu from their own inline script, which
        // may finish after this one. Keep this menu if that happens.
        new MutationObserver(() => {
          if (!isCurrent()) menu.replaceChildren(...sections);
        }).observe(menu, { childList: true });
      })
      .catch((error) => {
        // Whatever menu the page already has stays in place.
        console.warn("Unable to load Farama projects", error);
      });
  }

  // ---- Annual fundraiser ---------------------------------------------------

  // The banner decides for itself when to appear (every December).
  const fundraiser = document.createElement("script");
  fundraiser.src = `${site}/assets/fundraising/december-fundraiser.js`;
  document.head.append(fundraiser);
})();
