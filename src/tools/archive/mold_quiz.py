"""Builds the mold illness quiz markup for the Resources page (questions from Xenia's original quiz)."""
import json, os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
MOLD = json.load(open(os.path.join(HERE, "quiz", "mold.json"), encoding="utf-8"))
FIX = {"Atriovenous abnormalities": "Arteriovenous abnormalities", "Blood-streaked mucous": "Blood-streaked mucus"}
STEPS = [
    ("cat1", "General &amp; respiratory symptoms", "Check everything you experience regularly."),
    ("cat2", "Digestive, immune &amp; nervous system", "Check everything you experience regularly."),
    ("cat3", "Medical &amp; exposure history", "Check any conditions you've been diagnosed with and any known exposures."),
]


def form():
    n = len(STEPS) + 1
    out = []
    steps = "".join(f'<li data-i="{i}"><span>{i + 1}</span>{lbl}</li>' for i, (_, lbl, _) in enumerate(STEPS))
    steps += f'<li data-i="{n - 1}"><span>{n}</span>Your results</li>'
    out.append(f'        <ol class="q-steps" aria-hidden="true">{steps}</ol>')
    for i, (cat, lbl, hint) in enumerate(STEPS):
        opts = "\n".join(
            f'            <label class="q-opt"><input type="checkbox" name="{cat}" value="{escape(FIX.get(v, v))}"><span>{escape(FIX.get(v, v))}</span></label>'
            for v in MOLD[cat])
        hidden = "" if i == 0 else " hidden"
        back = '<button type="button" class="btn btn-line" data-q="back">&larr; Back</button>' if i else "<span></span>"
        out.append(
            f'        <fieldset class="q-step" data-step="{i}"{hidden}>\n'
            f'          <legend><span class="q-num">Step {i + 1} of {n}</span>{lbl}</legend>\n'
            f'          <p class="q-hint">{hint} <b class="q-count">0 selected</b></p>\n'
            f'          <div class="q-opts">\n{opts}\n          </div>\n'
            f'          <div class="q-nav">{back}<button type="button" class="btn btn-dark" data-q="next">Next <span class="arrow">&rarr;</span></button></div>\n'
            f'        </fieldset>')
    out.append(
        f'        <fieldset class="q-step" data-step="{n - 1}" hidden>\n'
        f'          <legend><span class="q-num">Step {n} of {n}</span>Where should we send your results?</legend>\n'
        '          <p class="q-hint">Your score shows right away. A copy of your answers goes to Xenia so she can follow up if you\'d like.</p>\n'
        '          <div class="q-email">\n'
        '            <label for="mq-email">Email</label>\n'
        '            <input type="email" id="mq-email" name="email" autocomplete="email" placeholder="you@email.com" required>\n'
        '            <p class="q-err" id="mq-err" hidden>Please enter a valid email address.</p>\n'
        '          </div>\n'
        '          <div class="q-nav"><button type="button" class="btn btn-line" data-q="back">&larr; Back</button>'
        '<button type="submit" class="btn btn-dark">See my results <span class="arrow">&rarr;</span></button></div>\n'
        '        </fieldset>')
    return "\n".join(out)


def panel():
    return f'''
    <!-- MOLD QUIZ -->
    <div class="quiz-panel" id="mold-quiz" hidden>
      <div class="quiz-top">
        <div>
          <p class="eyebrow">Mold illness quiz</p>
          <h2>Could <em>mold</em> be behind your symptoms?</h2>
          <p class="lede">Three short checklists, about 5 minutes. Check what applies, then see your mold risk score.</p>
        </div>
        <button type="button" class="q-close" data-close-quiz aria-label="Close the quiz">&times;</button>
      </div>
      <form class="quiz" id="moldQuiz" novalidate>
{form()}
      </form>
      <div class="q-result" id="mq-result" hidden aria-live="polite">
        <p class="eyebrow">Your results</p>
        <div class="q-score"><b id="mq-score">0</b><span>Risk score</span></div>
        <h3 id="mq-level"></h3>
        <p id="mq-msg"></p>
        <div class="btn-row">
          <a class="btn btn-dark" href="https://l.bttr.to/7uRty" target="_blank" rel="noopener">Book a mold detox consult <span class="arrow">&rarr;</span></a>
          <a class="btn btn-line" href="/functional-medicine-lab-testing#mycotoxin">Order a mycotoxin test</a>
          <a class="btn btn-line js-book" href="#" target="_blank" rel="noopener">Book a free call</a>
        </div>
        <p class="fine" id="mq-note" hidden></p>
        <p class="fine">This quiz is a screening tool, not a diagnosis. <button type="button" class="q-link" data-q="restart">Retake the quiz</button></p>
      </div>
    </div>
'''


THYROID = [
    ("Do you frequently feel tired, even after a full night's sleep?", ["Yes, I'm often exhausted", "Sometimes, depending on the day", "No, I usually feel rested"]),
    ("Have you noticed changes in your weight despite no major diet or lifestyle changes?", ["Yes, my weight won't budge", "Somewhat, it's been harder to manage", "No, my weight is stable"]),
    ("Do you struggle with cold hands and feet, or feel cold when others don't?", ["Yes, I'm often cold", "Occasionally", "Rarely or never"]),
    ("Are you experiencing hair thinning, hair loss or dry skin?", ["Yes, it's noticeable", "A little", "No, not at all"]),
    ("Do you have trouble focusing or remembering things, or feel mentally foggy?", ["Yes, very often", "Sometimes", "No, my focus is fine"]),
]


def thyroid_panel(guide_url):
    qs = []
    for i, (q, opts) in enumerate(THYROID, 1):
        o = "".join(
            f'<label class="q-opt"><input type="radio" name="q{i}" value="{v}"><span>{escape(t)}</span></label>'
            for v, t in zip("ABC", opts))
        qs.append(
            f'        <fieldset class="q-q">\n'
            f'          <legend><span class="q-num">Question {i} of {len(THYROID)}</span>{escape(q)}</legend>\n'
            f'          <div class="q-opts">{o}</div>\n'
            f'        </fieldset>')
    body = "\n".join(qs)
    return f'''
    <!-- THYROID QUIZ -->
    <div class="quiz-panel" id="thyroid-quiz" hidden>
      <div class="quiz-top">
        <div>
          <p class="eyebrow">Thyroid health quiz</p>
          <h2>Could your symptoms be related to your <em>thyroid?</em></h2>
          <p class="lede">Five questions, about one minute. Pick the answer that fits you best.</p>
        </div>
        <button type="button" class="q-close" data-close-quiz aria-label="Close the quiz">&times;</button>
      </div>
      <form class="quiz" id="thyroidQuiz" novalidate>
{body}
        <p class="q-err" id="tq-err" hidden>Please answer all five questions.</p>
        <div class="q-nav"><span></span><button type="submit" class="btn btn-dark">Get my results <span class="arrow">&rarr;</span></button></div>
      </form>
      <div class="q-result" id="tq-result" hidden aria-live="polite">
        <p class="eyebrow">Your results</p>
        <h3 id="tq-level"></h3>
        <p id="tq-msg"></p>
        <div class="btn-row">
          <a class="btn btn-dark js-book" href="#" target="_blank" rel="noopener">Book a free call <span class="arrow">&rarr;</span></a>
          <a class="btn btn-line" href="{guide_url}" target="_blank" rel="noopener">Thyroid health guide (PDF)</a>
          <a class="btn btn-line" href="/functional-medicine-austin">Functional medicine</a>
        </div>
        <p class="fine">This quiz is a screening tool, not a diagnosis. <button type="button" class="q-link" data-q="restart">Retake the quiz</button></p>
      </div>
    </div>
'''
