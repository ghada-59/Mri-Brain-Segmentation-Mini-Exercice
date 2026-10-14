import { useEffect, useRef, useState } from "react";
import { Activity, ArrowRight, Check, CircleAlert, Layers3, LoaderCircle, Moon, Scan, ShieldCheck, Sun, Upload, X } from "lucide-react";

const API = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
export default function App() {
  const input = useRef(null);
  const [theme, setTheme] = useState(() => localStorage.getItem("contour-theme") || "dark");
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [api, setApi] = useState("checking");

  useEffect(() => { document.documentElement.dataset.theme = theme; localStorage.setItem("contour-theme", theme); }, [theme]);
  useEffect(() => {
    fetch(API + "/api/health").then((r) => { if (!r.ok) throw new Error(); return r.json(); })
      .then(() => setApi("online")).catch(() => setApi("offline"));
  }, []);
  useEffect(() => {
    if (!file) { setPreview(""); return undefined; }
    const url = URL.createObjectURL(file); setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  function choose(next) {
    setError(""); setResult(null);
    if (!next) return;
    if (!["image/png","image/jpeg","image/bmp","image/tiff"].includes(next.type) && !/\.(png|jpe?g|bmp|tiff?)$/i.test(next.name)) {
      setError("Choose a PNG, JPG, BMP or TIFF image."); return;
    }
    if (next.size > 15 * 1024 * 1024) { setError("Maximum upload size is 15 MB."); return; }
    setFile(next);
  }

  async function run() {
    if (!file) { setError("Choose an MRI image first."); return; }
    setBusy(true); setError(""); setResult(null);
    const body = new FormData(); body.append("file", file);
    try {
      const response = await fetch(API + "/api/segment", { method: "POST", body });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.detail || "Segmentation failed.");
      setResult(data);
    } catch (e) { setError(e.message || "Could not connect to the segmentation API."); }
    finally { setBusy(false); }
  }

  const maxHistogram = result ? Math.max.apply(null, result.histogram) : 1;
  return <div className="contour-shell">
    <aside className="side">
      <a className="brand" href="#home"><span className="brand-icon"><Scan size={21}/></span><span><b>CONTOUR</b><small>STUDIO / MRI</small></span></a>
      <p className="nav-label">ANALYSIS</p>
      <div className="side-active"><Activity size={17}/> Intensity segmentation <span>01</span></div>
      <div className="side-note"><span className={"led " + api}/><b>{api === "online" ? "Processing API ready" : api === "checking" ? "Checking API…" : "API offline"}</b><small>Local educational workflow</small></div>
      <div className="side-bottom"><ShieldCheck size={14}/> Classical thresholding · Not diagnostic</div>
    </aside>
    <main className="content" id="home">
      <header className="top"><div><span>BIOMEDICAL IMAGING</span><i>/</i><strong>Brain MRI segmentation exercise</strong></div><button className="theme-btn" onClick={() => setTheme(theme === "dark" ? "light" : "dark")} aria-label="Toggle theme">{theme === "dark" ? <Sun size={17}/> : <Moon size={17}/>}</button></header>
      <section className="hero"><div className="hero-copy"><span className="overline">IMAGE PROCESSING / CLASSICAL METHODS</span><h1>See the image<br/><em>in regions.</em></h1><p>Explore intensity-based segmentation with Otsu thresholding and three-level quantile partitioning.</p></div><div className="hero-mark"><Layers3 size={43}/><span>2D / 01</span></div></section>
      {error && <div className="alert"><CircleAlert size={18}/><span>{error}</span><button onClick={() => setError("")} aria-label="Dismiss"><X size={15}/></button></div>}
      {api === "offline" && <div className="alert"><CircleAlert size={18}/><span>API unavailable. Start the Python service on port 8000 and refresh this page.</span></div>}
      <div className="section-heading"><span>01</span><h2>Image input</h2><small>UPLOAD · PREVIEW · PROCESS</small></div>
      <section className="input-grid">
        <div className="card input-card"><div className="card-head"><div><small>INPUT SOURCE</small><h3>Upload MRI image</h3></div><span className="num">A</span></div>
          <input ref={input} className="hidden" type="file" accept=".png,.jpg,.jpeg,.bmp,.tif,.tiff,image/*" onChange={(e) => choose(e.target.files && e.target.files[0])}/>
          {preview ? <div className="preview-box"><img src={preview} alt="Selected MRI preview"/><div className="file-row"><div><b>{file.name}</b><small>{(file.size / 1024).toFixed(0)} KB · local preview</small></div><button onClick={() => {setFile(null);setResult(null);if(input.current)input.current.value="";}} aria-label="Remove image"><X size={16}/></button></div><p className="loaded"><Check size={14}/> Preview loaded successfully</p></div> :
          <button className="drop" onClick={() => input.current && input.current.click()} onDragOver={(e) => e.preventDefault()} onDrop={(e) => {e.preventDefault();choose(e.dataTransfer.files && e.dataTransfer.files[0]);}}><span className="upload-icon"><Upload size={22}/></span><b>Drop an MRI image here</b><small>or browse local files</small><span className="formats">PNG · JPG · BMP · TIFF / 15 MB MAX</span></button>}
          {preview && <button className="replace" onClick={() => input.current && input.current.click()}><Upload size={14}/> Change image</button>}
        </div>
        <div className="card method-card"><div className="card-head"><div><small>SEGMENTATION METHODS</small><h3>Intensity partitioning</h3></div><span className="num">B</span></div>
          <div className="method-row"><span className="method-dot mint"/> <div><b>Otsu thresholding</b><small>Separates pixels into two intensity groups using an automatic threshold.</small></div><span className="method-tag">2 CLASSES</span></div>
          <div className="method-row"><span className="method-dot rose"/> <div><b>Quantile thresholds</b><small>Partitions intensity values using the 33rd and 66th percentiles.</small></div><span className="method-tag">3 CLASSES</span></div>
          <button className="run-btn" disabled={!file || busy || api !== "online"} onClick={run}>{busy ? <><LoaderCircle className="spin" size={17}/> Processing image…</> : <>Run segmentation <ArrowRight size={17}/></>}</button>
          <p className="method-hint">These methods group pixel intensities; they do not identify anatomical structures.</p>
        </div>
      </section>
      <div className="section-heading results-heading"><span>02</span><h2>Segmentation results</h2><small>{result ? result.width + " × " + result.height + " PX" : "RUN TO GENERATE OUTPUTS"}</small></div>
      {result ? <>
        <div className="threshold-metrics"><div className="metric"><small>OTSU THRESHOLD</small><b>{result.otsu_threshold.toFixed(4)}</b><span>Automatic threshold</span></div><div className="metric"><small>QUANTILE T1</small><b>{result.quantile_thresholds[0].toFixed(4)}</b><span>33rd percentile</span></div><div className="metric"><small>QUANTILE T2</small><b>{result.quantile_thresholds[1].toFixed(4)}</b><span>66th percentile</span></div></div>
        <div className="image-results">{[{label:"Original grayscale",src:result.original,tag:"INPUT"},{label:"Otsu · 2 classes",src:result.two_class,tag:"BINARY"},{label:"Quantile · 3 classes",src:result.three_class,tag:"LABEL MAP"}].map((item) => <article className="result-panel" key={item.tag}><div className="result-head"><b>{item.label}</b><span>{item.tag}</span></div><div className="result-image"><img src={item.src} alt={item.label}/></div></article>)}</div>
        <div className="card histogram-card"><div className="card-head"><div><small>INTENSITY DISTRIBUTION</small><h3>Grayscale histogram</h3></div><span className="num">32 BINS</span></div><div className="histogram">{result.histogram.map((value, i) => <div key={i} title={"Bin " + (i+1) + ": " + value} style={{height: Math.max(2, value / maxHistogram * 100) + "%"}}/>)}</div><div className="hist-labels"><span>LOW INTENSITY</span><span>HIGH INTENSITY</span></div></div>
        <div className="scope-note"><ShieldCheck size={17}/><p><b>Interpretation boundary</b><br/>{result.note} The displayed regions are based only on pixel intensity and are not validated tumour contours.</p></div>
      </> : <div className="empty"><Layers3 size={28}/><b>No segmentation output yet</b><span>Upload an image and run the existing thresholding methods to compare the original and generated label maps.</span></div>}
      <footer><span>CONTOUR STUDIO <i>/</i> MRI THRESHOLDING</span><span>ACADEMIC PRACTICE PROJECT · 2D ONLY</span></footer>
    </main>
  </div>;
}
