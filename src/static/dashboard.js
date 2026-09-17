const state = { token: localStorage.getItem("library_token"), admin: localStorage.getItem("library_admin"), books: [], borrowers: [] };
const $ = (selector) => document.querySelector(selector);

function message(text, isError = false) {
  const notice = $("#notice");
  notice.textContent = text;
  notice.classList.remove("hidden", "error");
  if (isError) notice.classList.add("error");
  window.clearTimeout(message.timer);
  message.timer = window.setTimeout(() => notice.classList.add("hidden"), 5000);
}

async function api(path, options = {}) {
  const headers = { ...(options.body ? { "Content-Type": "application/json" } : {}), ...(options.headers || {}) };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const response = await fetch(`/api${path}`, { ...options, headers });
  const body = await response.json().catch(() => ({ message: "The server returned an invalid response." }));
  if (!response.ok) throw new Error(body.message || "Request failed.");
  return body.data;
}

function optionList(select, values, label) {
  select.innerHTML = `<option value="">Select an option</option>${values.map(item => `<option value="${item.id}">${escapeHtml(label(item))}</option>`).join("")}`;
}

function escapeHtml(value) {
  const element = document.createElement("span");
  element.textContent = value ?? "";
  return element.innerHTML;
}

function displayDate(value) {
  return value ? new Date(value).toLocaleString() : "—";
}

async function refresh() {
  try {
    const results = await Promise.allSettled([
      api("/books"), api("/borrowers"), api("/borrows"), api("/reports/dashboard"),
    ]);
    const books = results[0].status === "fulfilled" ? results[0].value : [];
    const borrowers = results[1].status === "fulfilled" ? results[1].value : [];
    const borrows = results[2].status === "fulfilled" ? results[2].value : [];
    const report = results[3].status === "fulfilled" ? results[3].value : { active_borrows: 0, overdue_borrows: [], fines: [] };
    state.books = books;
    state.borrowers = borrowers;
    optionList($("#borrow-book"), books.filter(book => book.available_copies > 0), book => `${book.title} (${book.available_copies} available)`);
    optionList($("#borrower"), borrowers, borrower => `${borrower.name} — ${borrower.email}`);
    $("#books").innerHTML = books.map(book => `<tr><td>${escapeHtml(book.title)}</td><td>${escapeHtml(book.author)}</td><td>${escapeHtml(book.isbn || "—")}</td><td>${book.available_copies} / ${book.total_copies}</td></tr>`).join("") || `<tr><td colspan="4">No books yet.</td></tr>`;
    $("#borrows").innerHTML = borrows.map(borrow => `<tr><td>${escapeHtml(borrow.book_title)}</td><td>${escapeHtml(borrow.borrower_name)}</td><td>${displayDate(borrow.due_at)}</td><td>${borrow.returned_at ? "Returned" : "Active"}</td><td>${borrow.returned_at ? "" : `<button class="danger return" data-id="${borrow.id}">Return</button>`}</td></tr>`).join("") || `<tr><td colspan="5">No borrowing records yet.</td></tr>`;
    $("#active-count").textContent = report.active_borrows;
    $("#overdue-count").textContent = report.overdue_borrows.length;
    $("#fine-count").textContent = report.fines.length;
    $("#overdue-list").innerHTML = report.overdue_borrows.length ? report.overdue_borrows.map(item => `<div>${escapeHtml(item.book_title)} — ${escapeHtml(item.borrower_name)}</div>`).join("") : "No overdue books.";
    const failed = results.find(result => result.status === "rejected");
    if (failed) message("Some dashboard data could not be loaded. Books and borrowers are still available.", true);
  } catch (err) {
    if (String(err.message).includes("Authorization")) logout();
    message(err.message, true);
  }
}

function logout() {
  localStorage.removeItem("library_token");
  localStorage.removeItem("library_admin");
  state.token = null;
  $("#app").classList.add("hidden");
  $("#login-card").classList.remove("hidden");
  $("#logout").classList.add("hidden");
}

$("#login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const data = await api("/auth/login", { method: "POST", body: JSON.stringify({ username: $("#username").value.trim(), password: $("#password").value }) });
    state.token = data.token;
    state.admin = data.admin.username;
    localStorage.setItem("library_token", state.token);
    localStorage.setItem("library_admin", state.admin);
    startApp();
  } catch (err) { message(err.message, true); }
});

$("#book-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  try { await api("/books", { method: "POST", body: JSON.stringify(Object.fromEntries(form)) }); event.currentTarget.reset(); message("Book added."); refresh(); } catch (err) { message(err.message, true); }
});

$("#borrower-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  try { await api("/borrowers", { method: "POST", body: JSON.stringify(Object.fromEntries(form)) }); event.currentTarget.reset(); message("Borrower added."); refresh(); } catch (err) { message(err.message, true); }
});

$("#borrow-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = Object.fromEntries(new FormData(event.currentTarget));
  form.due_at = new Date(form.due_at).toISOString();
  try { await api("/borrows", { method: "POST", body: JSON.stringify(form) }); event.currentTarget.reset(); message("Borrowing recorded."); refresh(); } catch (err) { message(err.message, true); }
});

document.addEventListener("click", async (event) => {
  if (event.target.matches(".refresh")) refresh();
  if (event.target.matches(".return")) {
    try { await api(`/borrows/${event.target.dataset.id}/return`, { method: "POST" }); message("Book returned."); refresh(); } catch (err) { message(err.message, true); }
  }
});
$("#logout").addEventListener("click", logout);

function startApp() {
  $("#login-card").classList.add("hidden");
  $("#app").classList.remove("hidden");
  $("#logout").classList.remove("hidden");
  $("#welcome").textContent = `Signed in as ${state.admin}.`;
  refresh();
}

if (state.token) startApp();
