const navToggle = document.querySelector("#nav-toggle");

if (navToggle) {
  document.querySelectorAll("#site-nav a").forEach((link) => {
    link.addEventListener("click", () => {
      navToggle.checked = false;
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") navToggle.checked = false;
  });
}

const form = document.querySelector("#quote-form");
if (form) initQuoteForm(form);

const motionOk = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
if (motionOk && "IntersectionObserver" in window) {
  const cards = document.querySelectorAll(".service, .step, .plate");
  cards.forEach((card, index) => {
    card.classList.add("reveal");
    card.style.setProperty("--d", `${(index % 3) * 70}ms`);
  });
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.18 }
  );
  cards.forEach((card) => observer.observe(card));
}

function quoteMode() {
  const raw = String(window.NBARCH_CONFIG?.formEndpoint ?? "").trim();
  if (!raw) return { type: "closed" };
  if (/^https?:\/\//i.test(raw)) {
    try {
      const url = new URL(raw);
      if (url.protocol === "http:" || url.protocol === "https:") {
        return { type: "http", value: url.toString() };
      }
    } catch {
      return { type: "invalid" };
    }
  }
  if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(raw)) {
    return { type: "mailto", value: raw };
  }
  return { type: "invalid" };
}

function initQuoteForm(form) {
  const status = document.querySelector("#quote-status");
  const success = document.querySelector("#quote-success");
  const submit = form.querySelector("[type='submit']");
  const fileInput = form.querySelector("#artwork");
  const artworkHint = document.querySelector("#artwork-hint");
  const another = document.querySelector("#quote-another");
  const MAX_FILE = 8 * 1024 * 1024;
  const ALLOWED = new Set(["svg", "pdf", "ai", "eps", "png", "jpg", "jpeg", "webp"]);

  const closedCopy =
    "Online quotes are coming soon. This form shows what we’ll ask. Until a destination is connected, the button stays off and nothing you type is sent or stored.";
  const invalidCopy =
    "Online quotes aren’t open yet. The form setting isn’t a web address or an email, so submissions stay off and nothing you type is sent or stored.";
  const httpCopy =
    "Send the piece, the quantity, and the mark you want. You’ll approve a proof before anything is engraved.";

  function mailtoCopy(address) {
    return `Submitting opens your email app with this request filled in, addressed to ${address}. If you chose artwork, attach that file in the email — the browser can’t add it. Nothing is stored on this website.`;
  }

  function applyMode() {
    const mode = quoteMode();
    const live = mode.type === "http" || mode.type === "mailto";
    submit.disabled = !live;
    submit.textContent = mode.type === "mailto" ? "Open email to send" : "Submit quote request";
    if (mode.type === "http") status.textContent = httpCopy;
    else if (mode.type === "mailto") status.textContent = mailtoCopy(mode.value);
    else if (mode.type === "invalid") status.textContent = invalidCopy;
    else status.textContent = closedCopy;
    artworkHint.textContent =
      mode.type === "mailto"
        ? "SVG, PDF, AI, EPS, or PNG. You’ll attach it yourself in the email. Optional."
        : "SVG, PDF, AI, EPS, or PNG, up to 8 MB. Optional.";
    return mode;
  }

  function clearErrors() {
    form.querySelectorAll(".field-error").forEach((node) => {
      node.hidden = true;
      node.textContent = "";
    });
    form.querySelectorAll("[aria-invalid]").forEach((node) => {
      node.removeAttribute("aria-invalid");
    });
  }

  function setError(id, message) {
    const field = document.getElementById(id);
    const error = document.getElementById(`${id}-error`);
    error.hidden = false;
    error.textContent = message;
    field.setAttribute("aria-invalid", "true");
    if (!field.getAttribute("aria-describedby")?.includes(error.id)) {
      const described = field.getAttribute("aria-describedby");
      field.setAttribute("aria-describedby", described ? `${described} ${error.id}` : error.id);
    }
    return field;
  }

  function validate() {
    clearErrors();
    const errors = [];
    const name = form.name.value.trim();
    const email = form.email.value.trim();
    const phone = form.phone.value.trim();
    const product = form.product.value;
    const quantity = form.quantity.value.trim();
    const description = form.description.value.trim();
    const file = fileInput.files?.[0];

    if (name.length < 2) errors.push(setError("name", "Enter your name."));
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errors.push(setError("email", "Enter an email address we can reply to."));
    }
    if (phone && (phone.replace(/\D/g, "").length < 7 || !/^[0-9+().\-\s]+$/.test(phone))) {
      errors.push(setError("phone", "Check the phone number, or leave it blank."));
    }
    if (!product) errors.push(setError("product", "Choose a product type."));
    if (!/^[1-9]\d{0,5}$/.test(quantity)) {
      errors.push(setError("quantity", "Enter a quantity of at least 1."));
    }
    if (description.length < 12) {
      errors.push(setError("description", "Describe the piece and what should be engraved."));
    }
    if (file) {
      const ext = file.name.split(".").pop()?.toLowerCase() ?? "";
      if (!ALLOWED.has(ext)) {
        errors.push(setError("artwork", "Use an SVG, PDF, AI, EPS, PNG, JPG, or WebP file."));
      } else if (file.size > MAX_FILE) {
        errors.push(setError("artwork", "That file is over 8 MB. Send a smaller one."));
      }
    }
    if (errors.length) errors[0].focus();
    return errors.length === 0;
  }

  function showSuccess(message) {
    success.querySelector("p").textContent = message;
    form.hidden = true;
    status.hidden = true;
    success.hidden = false;
    success.focus();
  }

  another?.addEventListener("click", () => {
    form.reset();
    clearErrors();
    success.hidden = true;
    form.hidden = false;
    status.hidden = false;
    applyMode();
    form.querySelector("#name")?.focus();
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const mode = applyMode();
    if (mode.type !== "http" && mode.type !== "mailto") {
      status.hidden = false;
      status.focus?.();
      return;
    }
    if (form.nb_leave_blank.value) {
      showSuccess("Thanks. If this was a real request, send it again without the extra website field.");
      return;
    }
    if (!validate()) return;

    if (mode.type === "mailto") {
      const file = fileInput.files?.[0];
      const body = [
        `Name: ${form.name.value.trim()}`,
        `Email: ${form.email.value.trim()}`,
        `Phone: ${form.phone.value.trim() || "(none)"}`,
        `Product: ${form.product.value}`,
        `Quantity: ${form.quantity.value.trim()}`,
        `Artwork: ${file ? `${file.name} (attach this file in your email app)` : "(none)"}`,
        "",
        form.description.value.trim(),
      ].join("\n");
      const href = `mailto:${mode.value}?subject=${encodeURIComponent("Quote request — N.B. Arch Co.")}&body=${encodeURIComponent(body)}`;
      window.location.href = href;
      status.hidden = false;
      status.textContent = file
        ? `Your email app should open with this request. Attach “${file.name}” before you send. Nothing was stored on this website.`
        : "Your email app should open with this request. Send it from there. Nothing was stored on this website.";
      return;
    }

    const originalLabel = submit.textContent;
    submit.disabled = true;
    submit.textContent = "Sending…";
    try {
      const payload = new FormData(form);
      payload.delete("nb_leave_blank");
      const response = await fetch(mode.value, {
        method: "POST",
        body: payload,
        headers: { Accept: "application/json" },
      });
      if (!response.ok) throw new Error(String(response.status));
      form.reset();
      showSuccess("Your request was sent. We’ll reply at the email you entered, with a proof before anything is engraved.");
    } catch {
      status.hidden = false;
      status.textContent = "We couldn’t send that. Your details are still in the form — try again in a moment.";
      submit.disabled = false;
      submit.textContent = originalLabel;
    }
  });

  applyMode();
}
