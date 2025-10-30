import React, { useState, useEffect } from "react";
import { FaMicrophone, FaVolumeUp, FaGlobe } from "react-icons/fa";


/**
 * Translingo – Modern AI Translator
 * Features:
 *  - Text translation (via Flask backend)
 *  - Speech input using Web Speech API
 *  - Speech output (speak translation)
 *  - Pastel cyberpunk UI with animated header
 *  - Output appears below input box (left), tips/notes on right
 */

export default function App() {
    // ---------------- STATES ----------------
    const [text, setText] = useState(""); // user input
    const [target, setTarget] = useState("hi"); // target language code
    const [result, setResult] = useState(null); // translated result
    const [loading, setLoading] = useState(false); // show "Translating..."
    const [showResult, setShowResult] = useState(false); // for animation
    const [lineVisible, setLineVisible] = useState([false, false, false]); // reveal animation per line
    const [listening, setListening] = useState(false); // mic state
    const [blink, setBlink] = useState(false); // mascot blink
    const [hueShift, setHueShift] = useState(0); // animated title hue

    // ---------------- EFFECTS ----------------
    // Animate header letters
    useEffect(() => {
        const id = setInterval(() => setHueShift((s) => (s + 1) % 360), 80);
        return () => clearInterval(id);
    }, []);

    // Mascot blinking when loading
    useEffect(() => {
        if (!loading) return;
        const t = setInterval(() => setBlink((b) => !b), 500);
        return () => clearInterval(t);
    }, [loading]);

    // ---------------- FUNCTIONS ----------------
    // Translate text using backend API
    async function handleTranslate() {
    if (!text.trim()) return;
    setLoading(true);
    setShowResult(false);
    setLineVisible([false, false, false]);

    try {
        const res = await fetch("/api/translate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, target }),
        });

        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

        const data = await res.json();
        setResult(data);

        // animate result reveal
        setTimeout(() => {
            setShowResult(true);
            [0, 1, 2].forEach((i) =>
                setTimeout(
                    () =>
                        setLineVisible((prev) => {
                            const copy = [...prev];
                            copy[i] = true;
                            return copy;
                        }),
                    i * 250
                )
            );
        }, 80);
    } catch (err) {
        console.error("Translation failed:", err);
        alert("Translation failed. Check console for details.");
    } finally {
        setLoading(false);
        setShowResult(true);
    }
}


    // Use browser speech recognition to fill input box
    function handleSpeechInput() {
        if (!("webkitSpeechRecognition" in window)) {
            alert("Speech recognition not supported in this browser.");
            return;
        }
        const recognition = new window.webkitSpeechRecognition();
        recognition.lang = "auto";
        recognition.start();
        setListening(true);

        recognition.onresult = (event) => {
            const spokenText = event.results[0][0].transcript;
            setText(spokenText);
            setListening(false);
        };

        recognition.onerror = () => {
            setListening(false);
        };
    }

    // Speak the translated text aloud
    function speakText(text) {
        if (!window.speechSynthesis) {
            alert("Speech synthesis not supported in this browser.");
            return;
        }
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = target;
        window.speechSynthesis.speak(utterance);
    }

    // ---------------- UI ----------------
    const title = "Translingo";

    return (
        <div style={styles.app}>
            {/* CSS animations for bubbles and glowing text */}
            <style>{keyframesCSS}</style>

            {/* Floating pastel bubbles */}
            <div style={styles.bubblesWrap}>
                <div className="bubble b1" style={styles.bubble} />
                <div className="bubble b2" style={styles.bubble} />
                <div className="bubble b3" style={styles.bubble} />
                <div className="bubble b4" style={styles.bubble} />
            </div>

            <div style={styles.container}>
                {/* Header with animated title and mascot */}
                <header style={styles.header}>
                    <div style={styles.titleRow}>
                        <h1 style={styles.title}>
                            {title.split("").map((ch, i) => {
                                const hue = (i * 20 + hueShift) % 360;
                                const color = `hsl(${hue}, 70%, 75%)`;
                                const shadowColor = `hsla(${hue}, 70%, 55%, 0.35)`;
                                return (
                                    <span
                                        key={i}
                                        style={{
                                            display: "inline-block",
                                            transform: `translateY(${Math.sin(
                                                (hueShift + i * 8) * (Math.PI / 180)
                                            ) * 4}px)`,
                                            transition: "transform 160ms linear",
                                            color,
                                            textShadow: `0 6px 18px ${shadowColor}`,
                                            fontWeight: 900,
                                            fontSize: "2.4rem",
                                            letterSpacing: "1px",
                                        }}
                                    >
                                        {ch}
                                    </span>
                                );
                            })}
                        </h1>

                        {/* Mascot face */}
                        <div style={styles.mascotWrap}>
                            <svg width="68" height="68" viewBox="0 0 64 64">
                                <defs>
                                    <linearGradient id="g1" x1="0" x2="1">
                                        <stop offset="0" stopColor="#FFB6C1" />
                                        <stop offset="1" stopColor="#87CEFA" />
                                    </linearGradient>
                                </defs>
                                <g>
                                    <rect
                                        x="6"
                                        y="10"
                                        rx="12"
                                        ry="12"
                                        width="52"
                                        height="44"
                                        fill="url(#g1)"
                                        opacity="0.95"
                                    />
                                    <circle cx="24" cy="28" r="5" fill="#fff" opacity="0.9" />
                                    <circle cx="40" cy="28" r="5" fill="#fff" opacity="0.9" />
                                    <circle cx="24" cy={blink ? 29 : 28} r="2" fill="#333" />
                                    <circle cx="40" cy="28" r="2" fill="#333" />
                                    <path
                                        d="M22 38 q6 6 20 0"
                                        stroke="#222"
                                        strokeWidth="2"
                                        strokeLinecap="round"
                                        fill="none"
                                        opacity="0.9"
                                    />
                                </g>
                            </svg>
                        </div>
                    </div>
                    <p style={styles.subtitle}>Translate. Romanize. Communicate.</p>
                </header>

                {/* --------- Main Card --------- */}
                <main style={styles.card}>
                    <div style={styles.mainRow}>
                        {/* LEFT SIDE — Input + Output */}
                        <div style={styles.leftColumn}>
                            <textarea
                                placeholder="Type or paste text here..."
                                value={text}
                                onChange={(e) => setText(e.target.value)}
                                style={styles.textarea}
                            />

                            {/* Output appears below input */}
                            <section
                                style={{
                                    ...styles.resultWrap,
                                    opacity: showResult ? 1 : 0,
                                    transform: showResult ? "translateY(0)" : "translateY(12px)",
                                }}
                            >
                                {result ? (
                                    <>
                                        <div
                                            style={{
                                                ...styles.resultLine,
                                                ...(lineVisible[0] ? styles.lineVisible : {}),
                                            }}
                                        >
                                            <strong style={{ color: "#FFB6C1" }}>Language:</strong>
                                            <span style={styles.resultText}>
                                                {result.source_lang}
                                            </span>
                                        </div>
                                        <div
                                            style={{
                                                ...styles.resultLine,
                                                ...(lineVisible[1] ? styles.lineVisible : {}),
                                            }}
                                        >
                                            <strong style={{ color: "#87CEFA" }}>Translation:</strong>
                                            <span style={styles.resultText}>{result.translated}</span>
                                        </div>
                                        <div
                                            style={{
                                                ...styles.resultLine,
                                                ...(lineVisible[2] ? styles.lineVisible : {}),
                                            }}
                                        >
                                            <strong style={{ color: "#FFD700" }}>Romanized:</strong>
                                            <span style={styles.resultText}>{result.romanized}</span>
                                        </div>
                                    </>
                                ) : (
                                    <div style={styles.placeholder}>
                                        Your translated output will appear here.
                                    </div>
                                )}
                            </section>
                        </div>

                        {/* RIGHT SIDE — Buttons + Tips */}
                        <div style={styles.sideColumn}>
                            <label style={styles.label}>Select Language</label>
                            <select
                                value={target}
                                onChange={(e) => setTarget(e.target.value)}
                                style={styles.select}
                            >
                                <option value="hi">Hindi</option>                              
                                <option value="en">English</option>
                                <option value="fr">French</option>
                                <option value="es">Spanish</option>
                                <option value="ja">Japanese</option>
                                <option value="tr">Turkish</option>
                                <option value="de">German</option>
                                <option value="nl">Dutch</option>
                                <option value="ko">Korean</option>
                                <option value="ru">Russian</option>
                                <option value="la">Latin</option>
                                <option value="zh-CN">Chinese</option>
                            </select>
                            <style>
                                {`
    select:focus {
      background: rgba(0, 0, 0, 0.7) !important;
      color: #fff !important;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255,255,255,0.4);
    }

    select:hover {
      background: rgba(255, 255, 255, 0.25);
    }
  `}
                            </style>


                            <div style={styles.actions}>
                                <button
                                    onClick={handleTranslate}
                                    disabled={loading}
                                    style={{
                                        ...styles.translateBtn,
                                        display: "flex",
                                        alignItems: "left",
                                        justifyContent: "left",
                                        gap: "35px",
                                    }}
                                >
                                    {loading ? (
                                        <>
                                            <FaGlobe />
                                            Translating...
                                        </>
                                    ) : (
                                        <>
                                            <FaGlobe />
                                            Translate
                                        </>
                                    )}
                                </button>

                                <button
                                    onClick={handleSpeechInput}
                                    disabled={loading}
                                    style={{
                                        ...styles.translateBtn,
                                        display: "flex",
                                        alignItems: "left",
                                        justifyContent: "left",
                                        gap: "46px",
                                    }}
                                >
                                    <FaMicrophone />
                                    {listening ? "Listening..." : "Speak"}
                                </button>

                                <button
                                    onClick={() => speakText(result?.translated || "")}
                                    disabled={!result}
                                    style={{
                                        ...styles.translateBtn,
                                        display: "flex",
                                        alignItems: "center",
                                        justifyContent: "left",
                                        gap: "46px",
                                        cursor: result ? "pointer" : "not-allowed",
                                        opacity: result ? 1 : 0.6,
                                    }}
                                >
                                    <FaVolumeUp /> Listen
                                </button>
                            </div>

                            {/* Helpful tips and notes */}
                            <div style={styles.hint}>
                                Tasks:<br/>
                                • Use short lines for better translation accuracy. <br />
                                • Keep background noise low when using the microphone. <br />
                                • Check that your microphone permission is enabled. <br />
                                • Don’t write Romanized text — the AI detects it as English. not the language you want.{" "}
                                <br />
                                <br />
                                Note: <br />
                                • Only 12 languages are available currently. <br />
                            </div>
                        </div>
                    </div>
                </main>

                {/* Footer */}
                <footer style={styles.footer}>
                    <div style={styles.small}>Local demo • React + Flask</div>
                    <div style={styles.small}>Made with ♥ — Fauzia’s Translingo</div>
                </footer>
            </div>
        </div>
    );
}

/* ---------- Styles ---------- */

const styles = {
    app: {
        minHeight: "100vh",
        background: "linear-gradient(120deg, #06113b 0%, #0b2546 35%, #071a36 100%)",
        padding: "48px 18px",
        display: "flex",
        justifyContent: "center",
        alignItems: "flex-start",
        fontFamily: "'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial",
        color: "#edf2ff",
    },
    bubblesWrap: {
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        overflow: "hidden",
        zIndex: 0,
    },
    bubble: {
        position: "absolute",
        borderRadius: "50%",
        filter: "blur(30px)",
        opacity: 0.7,
    },
    container: {
        position: "relative",
        zIndex: 2,
        width: "min(980px, 96%)",
    },
    header: {
        marginBottom: "18px",
        textAlign: "center",
    },
    titleRow: {
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: "18px",
    },
    title: {
        margin: 0,
        padding: 0,
        display: "inline-block",
    },
    mascotWrap: {
        width: 68,
        height: 68,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transform: "translateY(4px)",
    },
    subtitle: {
        marginTop: 8,
        color: "rgba(237,242,255,0.8)",
        fontSize: "14px",
        opacity: 0.9,
    },
    card: {
        background: "linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03))",
        borderRadius: "16px",
        padding: "20px",
        boxShadow: "0 10px 40px rgba(0,0,0,0.6)",
        border: "1px solid rgba(255,255,255,0.06)",
        backdropFilter: "blur(8px)",
    },
    topRow: {
        display: "flex",
        gap: "18px",
        alignItems: "flex-start",
        flexWrap: "wrap",
    },
    textarea: {
        flex: "1 1 56%",
        minHeight: 140,
        padding: 14,
        fontSize: 15,
        borderRadius: 12,
        border: "1px solid rgba(255,255,255,0.06)",
        background: "linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01))",
        color: "#eaf2ff",
        resize: "vertical",
        boxShadow: "inset 0 1px 0 rgba(255,255,255,0.02)",
    },
    sideColumn: {
        width: 180,
        display: "flex",
        flexDirection: "column",
        gap: 12,
    },
    label: {
        fontSize: 12,
        color: "rgba(237,242,255,0.9)",
        marginBottom: 4,
    },
    select: {
        padding: "10px 12px",
        borderRadius: 10,
        border: "1px solid rgba(255,255,255,0.25)",
        background: "#283F59",   // transparent glass effect
        color: "#fff",                           // white text when closed
        fontSize: 14,
        backdropFilter: "blur(10px)",            // adds that frosted-glass blur
        WebkitBackdropFilter: "blur(10px)",      // Safari compatibility
        transition: "all 0.3s ease",
        cursor: "pointer",
    },
    translateBtn: {
        marginTop: 8,
        padding: "10px 12px",
        borderRadius: 12,
        border: "none",
        cursor: "pointer",
        fontWeight: 700,
        background: "linear-gradient(90deg, #ffb6c1, #87cefa, #fff176)",
        color: "#081123",
        boxShadow: "0 8px 22px rgba(135,206,250,0.14)",
        transition: "transform 220ms ease, filter 220ms ease",
        minWidth: "185px",
        fontSize: "14px",  // or 15px, 17px — whatever looks good
        textAlign: "center",
        /* 👇 these make icons and text sit perfectly together */
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: "8px",
        lineHeight: 1, // prevents text from sitting lower than icons

    },
    translateBtnLoading: {
        filter: "brightness(0.95) saturate(0.9)",
        cursor: "progress",
    },
    hint: {
        fontSize: 12,
        color: "rgba(237,242,255,0.7)",
        marginTop: 6,
    },
    resultWrap: {
        marginTop: 18,
        padding: 16,
        borderRadius: 12,
        minHeight: 250,
        background: "linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01))",
        border: "1px solid rgba(255,255,255,0.04)",
        transition: "all 360ms ease",
    },
    resultLine: {
        display: "flex",
        gap: 12,
        alignItems: "center",
        marginBottom: 8,
        opacity: 0,
        transform: "translateY(8px)",
    },
    resultText: {
        marginLeft: 6,
        color: "rgba(237,242,255,0.95)",
    },
    lineVisible: {
        opacity: 1,
        transform: "translateY(0)",
        transition: "all 420ms cubic-bezier(.2,.9,.2,1)",
    },
    placeholder: {
        textAlign: "center",
        color: "rgba(237,242,255,0.6)",
    },
    mainRow: {
        display: "flex",
        gap: "18px",
        alignItems: "flex-start",
        flexWrap: "wrap",
    },
    leftColumn: {
        flex: "1 1 56%",
        display: "flex",
        flexDirection: "column",
        gap: "12px",
    },

    footer: {
        marginTop: 16,
        display: "flex",
        justifyContent: "space-between",
        color: "rgba(237,242,255,0.6)",
        fontSize: 12,
    },
    small: {
        opacity: 0.9,
    },

};

/* ---------- keyframes + bubble positions via CSS string ---------- */

const keyframesCSS = `
/* floating bubbles */
.bubble { opacity: 0.6; }
.b1 { width: 260px; height: 260px; left: -80px; top: -40px; background: radial-gradient(circle at 30% 30%, rgba(255,182,193,0.55), transparent 40%), radial-gradient(circle at 70% 70%, rgba(168,230,207,0.45), transparent 35%); animation: float1 10s ease-in-out infinite; }
.b2 { width: 180px; height: 180px; right: -60px; top: 20px; background: radial-gradient(circle at 30% 30%, rgba(255,249,179,0.45), transparent 40%), radial-gradient(circle at 70% 70%, rgba(135,206,250,0.35), transparent 35%); animation: float2 12s ease-in-out infinite; }
.b3 { width: 140px; height: 140px; left: 20%; bottom: -40px; background: radial-gradient(circle at 40% 40%, rgba(171,135,255,0.28), transparent 40%), radial-gradient(circle at 70% 70%, rgba(255,182,193,0.2), transparent 35%); animation: float3 9s ease-in-out infinite; }
.b4 { width: 220px; height: 220px; right: 8%; bottom: -60px; background: radial-gradient(circle at 30% 30%, rgba(168,230,207,0.4), transparent 40%), radial-gradient(circle at 70% 70%, rgba(255,255,179,0.25), transparent 35%); animation: float4 14s ease-in-out infinite; }

@keyframes float1 { 0% { transform: translateY(0) translateX(0) scale(1) } 50% { transform: translateY(18px) translateX(8px) scale(1.03) } 100% { transform: translateY(0) translateX(0) scale(1)} }
@keyframes float2 { 0% { transform: translateY(0) translateX(0) scale(1) } 50% { transform: translateY(-14px) translateX(-6px) scale(1.02) } 100% { transform: translateY(0) translateX(0) scale(1)} }
@keyframes float3 { 0% { transform: translateY(0) translateX(0) scale(1) } 50% { transform: translateY(12px) translateX(-10px) scale(1.01) } 100% { transform: translateY(0) translateX(0) scale(1)} }
@keyframes float4 { 0% { transform: translateY(0) translateX(0) scale(1) } 50% { transform: translateY(-20px) translateX(6px) scale(1.04) } 100% { transform: translateY(0) translateX(0) scale(1)} }

/* subtle glow underline (optional) */
.title-underline { position: relative; display: block; margin: 8px auto 0; width: 120px; height: 6px; border-radius: 8px; background: linear-gradient(90deg, rgba(255,182,193,0.9), rgba(168,230,207,0.9), rgba(255,255,179,0.9)); box-shadow: 0 8px 24px rgba(168,230,207,0.08); animation: glow 4s ease-in-out infinite; }
@keyframes glow { 0% { filter: hue-rotate(0deg) } 50% { filter: hue-rotate(30deg) } 100% { filter: hue-rotate(0deg) } }
`;

/* ---------- After-load: position bubbles (we set absolute positions by CSS classes, so nothing needed here) ---------- */

// Add small effect: show result container when result is set
// (Handled in the component via showResult state)
