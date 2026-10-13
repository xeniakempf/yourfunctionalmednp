// chart-request.js — the "Email me the chart" form on /clinicians
// Same flow as learn.bhrt.app (xeniakempf/learn-bhrt-app):
// 1) validates the email  2) saves it to the "bhrt-leads" blob store
// 3) emails the Estradiol Conversion Chart via Resend
//
// Environment variables (Netlify: Site configuration → Environment variables). Never put these in code:
//   RESEND_API_KEY  — required
//   NOTIFY_EMAIL    — optional; if set, a short "new chart request" note goes to this address
// Endpoint: POST /.netlify/functions/chart-request  { email, website (honeypot) }

import { getStore } from "@netlify/blobs";

const FROM = "BHRT Navigator <noreply@noreply.yourfunctional.health>";
const SITE = "https://www.yourfunctionalmednp.com";
const PDF_PATH = "/downloads/clinicians/estradiol-conversion-chart.pdf";
const COURSE_URL = "https://learn.bhrt.app";

export default async (req) => {
  if (req.method !== "POST") return json({ error: "Method not allowed" }, 405);

  let body;
  try { body = await req.json(); } catch { return json({ error: "Bad request" }, 400); }

  // Honeypot: real people never fill the hidden "website" field
  if (body.website) return json({ ok: true });

  const email = String(body.email || "").trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 254) {
    return json({ error: "Please enter a valid email address." }, 400);
  }
  if (!process.env.RESEND_API_KEY) {
    console.error("RESEND_API_KEY is not set");
    return json({ error: "We couldn't send the email just now. Please try again later." }, 503);
  }

  // Attach the PDF from this deploy (works on the test address and the real domain alike)
  const origin = new URL(req.url).origin;
  const pdfUrl = origin + PDF_PATH;
  const publicPdfUrl = (origin.includes("localhost") ? SITE : origin) + PDF_PATH;

  // Save the lead (one record per email; repeat requests update the timestamp)
  try {
    const leads = getStore("bhrt-leads");
    const existing = await leads.get(email, { type: "json", consistency: "strong" }).catch(() => null);
    await leads.setJSON(email, {
      email,
      firstRequestedAt: existing?.firstRequestedAt || new Date().toISOString(),
      lastRequestedAt: new Date().toISOString(),
      requests: (existing?.requests || 0) + 1,
      source: "estradiol-chart (yourfunctionalmednp.com/clinicians)",
    });
  } catch (err) {
    console.error("Blob write failed:", err); // don't block the email over a storage hiccup
  }

  const resp = await sendEmail({
    from: FROM,
    to: [email],
    subject: "Your Estradiol Conversion Chart",
    html: emailHtml(publicPdfUrl),
    text: emailText(publicPdfUrl),
    attachments: [{ path: pdfUrl, filename: "Estradiol_Conversion_Chart.pdf" }],
  });
  if (!resp.ok) {
    console.error("Resend error:", await resp.text());
    return json({ error: "We couldn't send the email just now. Please try again in a minute." }, 502);
  }

  if (process.env.NOTIFY_EMAIL) {
    await sendEmail({
      from: FROM,
      to: [process.env.NOTIFY_EMAIL],
      subject: "New chart request: " + email,
      text: `${email} requested the Estradiol Conversion Chart on yourfunctionalmednp.com/clinicians.`,
    }).catch((e) => console.error("Notify failed:", e));
  }

  return json({ ok: true });
};

function sendEmail(payload) {
  return fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { "Content-Type": "application/json" } });
}

function emailHtml(pdfUrl) {
  return `
  <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:560px;margin:0 auto;color:#16232A;line-height:1.5">
    <p style="font-family:Georgia,serif;font-size:20px;color:#083F39;margin:0 0 16px">Your Estradiol Conversion Chart</p>
    <p>The chart is attached to this email as a PDF, and you can also download it here:</p>
    <p style="margin:20px 0">
      <a href="${pdfUrl}" style="display:inline-block;background:#083F39;color:#F3FBF8;text-decoration:none;font-weight:700;padding:12px 20px;border-radius:10px">Download the chart (PDF)</a>
    </p>
    <p>It covers labeled dose to expected serum estradiol for every patch, gel, spray, oral, and vaginal product, with the brand-to-brand spread called out where the labels disagree. Print it, keep it at the desk, forward it to a colleague.</p>
    <p>The chart is one page from <a href="${COURSE_URL}" style="color:#0B5D53">BHRT Navigator</a>, a point-of-care reference app for prescribers. The app adds injectable estradiol, the full Rx Cards, lab interpretation, and male protocols, and pairs with a complete BHRT course if you want the framework behind the numbers.</p>
    <p style="margin-top:28px;font-size:13px;color:#54666C">Educational content for licensed clinicians. Not a substitute for clinical judgment, current package labeling, or informed consent with your patients.</p>
    <p style="font-size:12px;color:#8B9A9C">You're receiving this because you requested the chart at yourfunctionalmednp.com. We'll send updates about the course and app now and then; reply to this email with &quot;unsubscribe&quot; anytime and we'll take you off the list.</p>
  </div>`;
}

function emailText(pdfUrl) {
  return `Your Estradiol Conversion Chart

The chart is attached as a PDF, and you can also download it here:
${pdfUrl}

It covers labeled dose to expected serum estradiol for every patch, gel, spray, oral, and vaginal product, with the brand-to-brand spread called out where the labels disagree.

The chart is one page from BHRT Navigator, a point-of-care reference app for prescribers: ${COURSE_URL}

Educational content for licensed clinicians. Not a substitute for clinical judgment, current package labeling, or informed consent with your patients.

You're receiving this because you requested the chart at yourfunctionalmednp.com. We'll send updates about the course and app now and then; reply with "unsubscribe" anytime and we'll take you off the list.`;
}
