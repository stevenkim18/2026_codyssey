const portfolioConfig = {
  githubUsername: "stevenkim18",
  projectLimit: 6,
};

const body = document.body;
const header = document.querySelector("#site-header");
const navToggle = document.querySelector(".nav-toggle");
const navMenu = document.querySelector("#primary-menu");
const themeToggle = document.querySelector(".theme-toggle");
const themeIcon = document.querySelector(".theme-icon");
const themeLabel = document.querySelector(".theme-label");
const backToTop = document.querySelector("#back-to-top");
const projectStatus = document.querySelector("#project-status");
const projectsGrid = document.querySelector("#projects-grid");
const projectError = document.querySelector("#project-error");
const retryProjects = document.querySelector("#retry-projects");
const contactForm = document.querySelector("#contact-form");
const formSuccess = document.querySelector("#form-success");

const setTheme = (theme) => {
  const isDark = theme === "dark";
  body.dataset.theme = isDark ? "dark" : "light";
  themeToggle.setAttribute("aria-pressed", String(isDark));
  themeToggle.setAttribute("aria-label", isDark ? "라이트 모드로 전환" : "다크 모드로 전환");
  themeIcon.textContent = isDark ? "☾" : "☼";
  themeLabel.textContent = isDark ? "Dark" : "Light";
  localStorage.setItem("portfolio-theme", isDark ? "dark" : "light");
};

const storedTheme = localStorage.getItem("portfolio-theme");
setTheme(storedTheme === "dark" ? "dark" : "light");

themeToggle.addEventListener("click", () => {
  const nextTheme = body.dataset.theme === "dark" ? "light" : "dark";
  setTheme(nextTheme);
});

const closeMobileMenu = () => {
  navMenu.classList.remove("active");
  navToggle.setAttribute("aria-expanded", "false");
  navToggle.setAttribute("aria-label", "메뉴 열기");
};

navToggle.addEventListener("click", () => {
  const isOpen = navMenu.classList.toggle("active");
  navToggle.setAttribute("aria-expanded", String(isOpen));
  navToggle.setAttribute("aria-label", isOpen ? "메뉴 닫기" : "메뉴 열기");
});

document.querySelectorAll(".nav-link, .logo, .scroll-cue").forEach((link) => {
  link.addEventListener("click", () => closeMobileMenu());
});

const updateScrollUI = () => {
  const scrollY = window.scrollY;
  header.classList.toggle("scrolled", scrollY >= 60);
  backToTop.hidden = scrollY < 300;
};

window.addEventListener("scroll", updateScrollUI, { passive: true });
updateScrollUI();

backToTop.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

const observer = new IntersectionObserver((entries) => {
  entries.forEach(({ target, isIntersecting }) => {
    if (isIntersecting) {
      target.classList.add("is-visible");
      observer.unobserve(target);
    }
  });
}, { threshold: 0.2 });

document.querySelectorAll(".reveal").forEach((element) => observer.observe(element));

const showProjectState = (state) => {
  projectStatus.hidden = state !== "loading";
  projectError.hidden = state !== "error";
  projectsGrid.hidden = state !== "success";
};

const createProjectCard = ({ name, description, html_url: htmlUrl, language, stargazers_count: stars, forks_count: forks }, index) => `
  <article class="project-card">
    <div class="project-top"><span>0${index + 1}</span><span aria-label="GitHub 저장소">↗</span></div>
    <h3>${name}</h3>
    <p>${description || "설명이 등록되지 않은 프로젝트입니다."}</p>
    <div class="project-footer"><span>${language || "Code"} · ★ ${stars} · ⑂ ${forks}</span><a class="project-link" href="${htmlUrl}" target="_blank" rel="noreferrer" aria-label="${name} 저장소 열기">↗</a></div>
  </article>`;

const loadProjects = async () => {
  showProjectState("loading");
  try {
    const response = await fetch(`https://api.github.com/users/${portfolioConfig.githubUsername}/repos?sort=updated&per_page=100`);
    if (!response.ok) throw new Error(`GitHub API responded with ${response.status}`);
    const repositories = await response.json();
    const visibleRepositories = repositories
      .filter(({ fork, archived }) => !fork && !archived)
      .slice(0, portfolioConfig.projectLimit);

    if (visibleRepositories.length === 0) {
      showProjectState("empty");
      projectStatus.hidden = false;
      projectStatus.innerHTML = "<span>표시할 프로젝트가 없습니다.</span>";
      return;
    }

    projectsGrid.innerHTML = visibleRepositories.map(createProjectCard).join("");
    showProjectState("success");
  } catch (error) {
    console.error("프로젝트를 불러오지 못했습니다.", error);
    showProjectState("error");
  }
};

retryProjects.addEventListener("click", loadProjects);
loadProjects();

const validationRules = {
  name: (value) => value.trim() ? "" : "이름을 입력해주세요.",
  email: (value) => {
    if (!value.trim()) return "이메일을 입력해주세요.";
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) ? "" : "올바른 이메일 형식을 입력해주세요.";
  },
  message: (value) => value.trim() ? "" : "메시지를 입력해주세요.",
};

const validateField = (field) => {
  const errorMessage = validationRules[field.name](field.value);
  const errorElement = document.querySelector(`#${field.name}-error`);
  field.closest(".form-field").classList.toggle("invalid", Boolean(errorMessage));
  field.setAttribute("aria-invalid", String(Boolean(errorMessage)));
  errorElement.textContent = errorMessage;
  return !errorMessage;
};

contactForm.querySelectorAll("input, textarea").forEach((field) => {
  field.addEventListener("input", () => {
    validateField(field);
    formSuccess.hidden = true;
  });
});

contactForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const fields = [...contactForm.querySelectorAll("input, textarea")];
  const isValid = fields.map(validateField).every(Boolean);
  if (!isValid) return;
  contactForm.reset();
  contactForm.querySelectorAll("input, textarea").forEach((field) => field.setAttribute("aria-invalid", "false"));
  formSuccess.hidden = false;
});

document.querySelector("#current-year").textContent = new Date().getFullYear();
