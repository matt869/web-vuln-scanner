# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
HOW TO RUN:
  1. Open PowerShell or any terminal
  2. cd to the folder that contains this file
       e.g.  cd C:\\Users\\profe\\Downloads
  3. python sort_visualizer.py
  4. Browser opens at http://127.0.0.1:8765
  5. Press Ctrl+C to stop
"""

import http.server
import threading
import webbrowser
import time

PORT = 8765

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SORT // VISUALIZER - 15 Algorithms</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Bebas+Neue&display=swap" rel="stylesheet">
<style>
  :root {
    --bg:#07080d; --panel:#0d0f1a; --border:#1a1f35;
    --accent:#00f5d4; --accent2:#f72585; --accent3:#fee440;
    --accent4:#7b2fff; --accent5:#ff9f1c;
    --text:#c8d4f0; --dim:#3a4060; --green:#3dff6e; --red:#ff4d6d;
  }
  *{margin:0;padding:0;box-sizing:border-box;}
  body{background:var(--bg);color:var(--text);font-family:'Share Tech Mono',monospace;min-height:100vh;overflow-x:hidden;}
  body::after{content:'';position:fixed;inset:0;pointer-events:none;z-index:999;
    background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.06) 2px,rgba(0,0,0,.06) 4px);}
  .bg-grid{position:fixed;inset:0;pointer-events:none;z-index:0;
    background-image:linear-gradient(rgba(0,245,212,.03) 1px,transparent 1px),
                     linear-gradient(90deg,rgba(0,245,212,.03) 1px,transparent 1px);
    background-size:40px 40px;animation:gridDrift 20s linear infinite;}
  @keyframes gridDrift{to{background-position:40px 40px;}}
  .app{position:relative;z-index:1;max-width:1280px;margin:0 auto;padding:18px 24px 48px;}

  header{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:20px;
    padding-bottom:14px;border-bottom:1px solid var(--border);flex-wrap:wrap;gap:10px;}
  .logo{font-family:'Bebas Neue',sans-serif;font-size:48px;line-height:1;letter-spacing:4px;color:#fff;
    text-shadow:0 0 30px rgba(0,245,212,.5),0 0 60px rgba(0,245,212,.2);}
  .logo span{color:var(--accent);}
  .tagline{font-size:10px;letter-spacing:3px;color:var(--dim);padding-bottom:5px;}
  .badge{font-family:'Bebas Neue',sans-serif;font-size:12px;letter-spacing:2px;padding:5px 12px;
    border:1px solid #3572a5;color:#3572a5;border-radius:3px;background:rgba(53,114,165,.1);align-self:center;}

  .main-tabs{display:flex;margin-bottom:18px;border-bottom:1px solid var(--border);}
  .main-tab{font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:2px;text-transform:uppercase;
    padding:10px 20px;border:1px solid transparent;border-bottom:none;background:transparent;
    color:var(--dim);cursor:pointer;transition:all .15s;margin-bottom:-1px;}
  .main-tab:hover{color:var(--accent);}
  .main-tab.active{border-color:var(--border);border-bottom-color:var(--bg);color:var(--accent);background:var(--bg);}
  .tab-panel{display:none;} .tab-panel.active{display:block;}

  .tier{display:inline-block;font-size:9px;letter-spacing:1px;padding:2px 7px;border-radius:2px;
    margin-left:6px;vertical-align:middle;border:1px solid;}
  .tier-fast{border-color:rgba(61,255,110,.4);color:var(--green);background:rgba(61,255,110,.07);}
  .tier-med {border-color:rgba(254,228,64,.4);color:var(--accent3);background:rgba(254,228,64,.07);}
  .tier-slow{border-color:rgba(247,37,133,.4);color:var(--accent2);background:rgba(247,37,133,.07);}
  .tier-real{border-color:rgba(0,245,212,.6);color:var(--accent);background:rgba(0,245,212,.12);
    box-shadow:0 0 8px rgba(0,245,212,.2);}

  .stats-bar{display:flex;gap:18px;flex-wrap:wrap;padding:12px 18px;background:var(--panel);
    border:1px solid var(--border);border-radius:4px;margin-bottom:14px;}
  .stat{display:flex;flex-direction:column;gap:2px;}
  .stat-label{font-size:9px;letter-spacing:2px;color:var(--dim);text-transform:uppercase;}
  .stat-value{font-size:20px;color:var(--accent);text-shadow:0 0 12px rgba(0,245,212,.6);min-width:80px;}
  .stat-div{width:1px;background:var(--border);align-self:stretch;}
  .algo-name{font-family:'Bebas Neue',sans-serif;font-size:22px;color:var(--accent3);letter-spacing:2px;
    text-shadow:0 0 15px rgba(254,228,64,.4);margin-left:auto;align-self:center;}

  .group-label{font-size:9px;letter-spacing:2px;color:var(--dim);text-transform:uppercase;
    margin-bottom:6px;margin-top:10px;}
  .group-label:first-child{margin-top:0;}
  .algo-group{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:4px;}
  .controls{display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start;margin-bottom:14px;}
  .algo-panel{display:flex;flex-direction:column;}

  .btn{font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:1px;text-transform:uppercase;
    padding:6px 12px;border:1px solid var(--border);background:var(--panel);color:var(--dim);
    cursor:pointer;transition:all .15s;border-radius:3px;white-space:nowrap;}
  .btn:hover{border-color:var(--accent);color:var(--accent);box-shadow:0 0 8px rgba(0,245,212,.12);}
  .btn.active{border-color:var(--accent);color:var(--bg);background:var(--accent);}
  .btn.real{border-color:rgba(0,245,212,.4);}
  .btn.real.active{box-shadow:0 0 16px rgba(0,245,212,.5);}
  .btn.primary{border-color:var(--accent);color:var(--accent);}
  .btn.primary:hover{background:var(--accent);color:var(--bg);}
  .btn.danger{border-color:var(--accent2);color:var(--accent2);}
  .btn.danger:hover{background:var(--accent2);color:#fff;}
  .btn:disabled{opacity:.3;cursor:not-allowed;}

  .right-controls{display:flex;flex-direction:column;gap:8px;margin-left:auto;}
  .slider-row{display:flex;align-items:center;gap:8px;}
  .slider-label{font-size:10px;color:var(--dim);letter-spacing:1px;white-space:nowrap;min-width:44px;}
  input[type=range]{-webkit-appearance:none;height:3px;background:var(--border);border-radius:2px;outline:none;cursor:pointer;width:100px;}
  input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:13px;height:13px;
    background:var(--accent);border-radius:50%;box-shadow:0 0 8px rgba(0,245,212,.6);}
  .slider-val{font-size:12px;color:var(--accent);min-width:24px;text-align:right;}
  .action-row{display:flex;gap:6px;}

  .viz-wrap{background:var(--panel);border:1px solid var(--border);border-radius:4px;
    padding:16px 16px 0;position:relative;overflow:hidden;}
  .viz-wrap::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,var(--accent4),var(--accent),var(--accent2),var(--accent3));
    animation:shimmer 3s linear infinite;background-size:200% 100%;}
  @keyframes shimmer{to{background-position:200% 0;}}
  #cv{width:100%;height:370px;display:block;}
  .legend{display:flex;gap:14px;padding:8px 0 10px;flex-wrap:wrap;}
  .li{display:flex;align-items:center;gap:6px;font-size:10px;letter-spacing:1px;color:var(--dim);}
  .ld{width:11px;height:11px;border-radius:2px;}
  .prog-track{height:3px;background:var(--border);border-radius:2px;overflow:hidden;}
  .prog-fill{height:100%;width:0%;background:linear-gradient(90deg,var(--accent4),var(--accent));
    transition:width .08s;box-shadow:0 0 8px rgba(0,245,212,.5);}

  .ticker{margin-top:10px;padding:8px 14px;background:rgba(0,0,0,.4);border-left:3px solid var(--dim);
    font-size:11px;color:var(--dim);letter-spacing:1px;min-height:30px;}
  .ticker.on{color:var(--accent);border-color:var(--accent);}
  .ticker.ok{color:var(--green);border-color:var(--green);}

  .cx{margin-top:14px;padding:12px 16px;background:var(--panel);border:1px solid var(--border);
    border-radius:4px;display:flex;gap:20px;align-items:center;flex-wrap:wrap;}
  .cx-title{font-family:'Bebas Neue',sans-serif;font-size:17px;letter-spacing:2px;color:var(--accent4);min-width:140px;}
  .cx-item{display:flex;flex-direction:column;gap:2px;}
  .cx-lbl{font-size:9px;color:var(--dim);letter-spacing:2px;}
  .cx-val{font-size:13px;color:var(--text);}

  .code-panel{padding:16px 18px;background:var(--panel);border:1px solid var(--border);border-radius:4px;}
  .code-panel h3{font-family:'Bebas Neue',sans-serif;font-size:17px;letter-spacing:2px;color:#3572a5;margin-bottom:10px;}
  .sub-tabs{display:flex;gap:4px;margin-bottom:10px;flex-wrap:wrap;}
  pre{background:#050709;border:1px solid #0d1220;border-radius:3px;padding:14px 16px;font-size:11.5px;line-height:1.75;overflow-x:auto;color:#abb2bf;}
  .kw{color:#c678dd;} .fn{color:#61afef;} .cm{color:#5c6370;font-style:italic;}
  .st{color:#98c379;} .nm{color:#d19a66;} .bi{color:#e06c75;} .de{color:#e5c07b;}

  .speed-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px;margin-bottom:16px;}
  .speed-card{background:var(--panel);border:1px solid var(--border);border-radius:4px;padding:16px;position:relative;overflow:hidden;}
  .speed-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
  .speed-card.real::before{background:var(--accent);}
  .speed-card.fast::before{background:var(--green);}
  .speed-card.med::before{background:var(--accent3);}
  .speed-card.slow::before{background:var(--accent2);}
  .sc-name{font-family:'Bebas Neue',sans-serif;font-size:19px;letter-spacing:2px;margin-bottom:3px;}
  .speed-card.real .sc-name{color:var(--accent);}
  .speed-card.fast .sc-name{color:var(--green);}
  .speed-card.med  .sc-name{color:var(--accent3);}
  .speed-card.slow .sc-name{color:var(--accent2);}
  .sc-used{font-size:10px;color:var(--dim);letter-spacing:1px;margin-bottom:10px;}
  .sc-bars{display:flex;flex-direction:column;gap:5px;}
  .sc-bar-row{display:flex;align-items:center;gap:8px;font-size:10px;}
  .sc-bar-label{min-width:52px;color:var(--dim);letter-spacing:1px;}
  .sc-bar-track{flex:1;height:8px;background:var(--border);border-radius:2px;overflow:hidden;}
  .sc-bar-fill{height:100%;border-radius:2px;}
  .sc-bar-val{min-width:70px;color:var(--text);text-align:right;}

  @media(max-width:600px){.logo{font-size:34px;}#cv{height:240px;}.speed-grid{grid-template-columns:1fr;}}
</style>
</head>
<body>
<div class="bg-grid"></div>
<div class="app">

<header>
  <div><div class="logo">SORT<span>//</span>VIZ</div></div>
  <div class="tagline">15 Algorithms &middot; Real-world Speed Comparison &middot; Python Server</div>
  <div class="badge">&#x1F40D; PYTHON &middot; ZERO DEPS</div>
</header>

<div class="main-tabs">
  <button class="main-tab active" data-tab="viz">&#9881; Visualizer</button>
  <button class="main-tab" data-tab="speed">&#9889; Speed Comparison</button>
  <button class="main-tab" data-tab="pycode">&#x1F40D; Python Code</button>
</div>

<!-- TAB 1: VISUALIZER -->
<div id="tab-viz" class="tab-panel active">
  <div class="stats-bar">
    <div class="stat"><div class="stat-label">Comparisons</div><div class="stat-value" id="s-cmp">0</div></div>
    <div class="stat-div"></div>
    <div class="stat"><div class="stat-label">Swaps / Writes</div><div class="stat-value" id="s-swp">0</div></div>
    <div class="stat-div"></div>
    <div class="stat"><div class="stat-label">Time (ms)</div><div class="stat-value" id="s-time">--</div></div>
    <div class="stat-div"></div>
    <div class="stat"><div class="stat-label">Array Size</div><div class="stat-value" id="s-sz">80</div></div>
    <div class="algo-name" id="a-disp">TIM SORT</div>
  </div>

  <div class="controls">
    <div class="algo-panel">
      <div class="group-label">&#x1F3C6; Real-world / Production (fastest &amp; most accurate)</div>
      <div class="algo-group" id="a-btns">
        <button class="btn real active" data-algo="tim">Tim Sort<span class="tier tier-real">PYTHON BUILT-IN</span></button>
        <button class="btn real" data-algo="intro">Intro Sort<span class="tier tier-real">C++ STD::SORT</span></button>
        <button class="btn real" data-algo="merge">Merge Sort<span class="tier tier-fast">FAST</span></button>
        <button class="btn real" data-algo="quick">Quick Sort<span class="tier tier-fast">FAST</span></button>
        <button class="btn real" data-algo="heap">Heap Sort<span class="tier tier-fast">FAST</span></button>
      </div>
      <div class="group-label">&#9889; Improved Classics</div>
      <div class="algo-group">
        <button class="btn" data-algo="shell">Shell Sort<span class="tier tier-med">MED</span></button>
        <button class="btn" data-algo="comb">Comb Sort<span class="tier tier-med">MED</span></button>
        <button class="btn" data-algo="cocktail">Cocktail Shaker<span class="tier tier-med">MED</span></button>
        <button class="btn" data-algo="counting">Counting Sort<span class="tier tier-fast">FAST (int)</span></button>
        <button class="btn" data-algo="radix">Radix Sort<span class="tier tier-fast">FAST (int)</span></button>
      </div>
      <div class="group-label">&#x1F4DA; Classic / Educational</div>
      <div class="algo-group">
        <button class="btn" data-algo="bubble">Bubble Sort<span class="tier tier-slow">SLOW</span></button>
        <button class="btn" data-algo="selection">Selection Sort<span class="tier tier-slow">SLOW</span></button>
        <button class="btn" data-algo="insertion">Insertion Sort<span class="tier tier-slow">SLOW</span></button>
        <button class="btn" data-algo="cycle">Cycle Sort<span class="tier tier-slow">MIN WRITES</span></button>
        <button class="btn" data-algo="bogo">Bogo Sort<span class="tier tier-slow">DON'T</span></button>
      </div>
    </div>
    <div class="right-controls">
      <div class="slider-row">
        <span class="slider-label">SIZE</span>
        <input type="range" id="sz-sl" min="10" max="150" value="80">
        <span class="slider-val" id="sz-v">80</span>
      </div>
      <div class="slider-row">
        <span class="slider-label">SPEED</span>
        <input type="range" id="sp-sl" min="1" max="100" value="70">
        <span class="slider-val" id="sp-v">70</span>
      </div>
      <div class="action-row">
        <button class="btn primary" id="btn-gen">&#8635; NEW</button>
        <button class="btn primary" id="btn-sort">&#9654; SORT</button>
        <button class="btn danger"  id="btn-stop" disabled>&#9632; STOP</button>
      </div>
      <div style="font-size:10px;color:var(--dim);letter-spacing:1px;margin-top:4px;">
        SPACE = sort/stop &nbsp; R = new array
      </div>
    </div>
  </div>

  <div class="viz-wrap">
    <canvas id="cv"></canvas>
    <div class="legend">
      <div class="li"><div class="ld" style="background:#1e2545;border:1px solid #3a4060"></div>Unsorted</div>
      <div class="li"><div class="ld" style="background:#00f5d4"></div>Active</div>
      <div class="li"><div class="ld" style="background:#f72585"></div>Swapping</div>
      <div class="li"><div class="ld" style="background:#fee440"></div>Pivot / Key</div>
      <div class="li"><div class="ld" style="background:#7b2fff"></div>Run boundary</div>
      <div class="li"><div class="ld" style="background:#3dff6e"></div>Sorted</div>
    </div>
    <div class="prog-track"><div class="prog-fill" id="pf"></div></div>
  </div>

  <div class="ticker" id="ticker">// Tim Sort and Intro Sort are the fastest -- press SORT or SPACE to begin</div>

  <div class="cx">
    <div class="cx-title" id="cx-name">TIM SORT</div>
    <div class="cx-item"><div class="cx-lbl">Best</div><div class="cx-val" id="cx-b">O(n)</div></div>
    <div class="cx-item"><div class="cx-lbl">Average</div><div class="cx-val" id="cx-a">O(n log n)</div></div>
    <div class="cx-item"><div class="cx-lbl">Worst</div><div class="cx-val" id="cx-w">O(n log n)</div></div>
    <div class="cx-item"><div class="cx-lbl">Space</div><div class="cx-val" id="cx-s">O(n)</div></div>
    <div class="cx-item"><div class="cx-lbl">Stable</div><div class="cx-val" id="cx-st">Yes</div></div>
    <div class="cx-item"><div class="cx-lbl">Used in</div><div class="cx-val" id="cx-u" style="color:var(--accent)">Python, Java, Android</div></div>
    <div class="cx-item" style="margin-left:auto">
      <div class="cx-lbl">Why it is fast</div>
      <div class="cx-val" id="cx-d" style="font-size:11px;max-width:360px;color:#7888aa">
        Detects natural runs in real data, uses insertion sort for small chunks and merge for large. Beats pure merge sort on real-world data.
      </div>
    </div>
  </div>
</div>

<!-- TAB 2: SPEED COMPARISON -->
<div id="tab-speed" class="tab-panel">
  <div class="speed-grid">
    <div class="speed-card real">
      <div class="sc-name">Tim Sort</div>
      <div class="sc-used">Used in: Python built-in sorted() / Java Arrays.sort() / Android</div>
      <div class="sc-bars">
        <div class="sc-bar-row"><span class="sc-bar-label">BEST</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:100%;background:var(--accent)"></div></div><span class="sc-bar-val">O(n)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">AVG</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:90%;background:var(--accent)"></div></div><span class="sc-bar-val">O(n log n)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">WORST</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:90%;background:var(--accent)"></div></div><span class="sc-bar-val">O(n log n)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">STABLE</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:100%;background:var(--green)"></div></div><span class="sc-bar-val">YES</span></div>
      </div>
    </div>
    <div class="speed-card real">
      <div class="sc-name">Intro Sort</div>
      <div class="sc-used">Used in: C++ std::sort / .NET / GNU C++ Library</div>
      <div class="sc-bars">
        <div class="sc-bar-row"><span class="sc-bar-label">BEST</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:95%;background:var(--accent)"></div></div><span class="sc-bar-val">O(n log n)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">AVG</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:92%;background:var(--accent)"></div></div><span class="sc-bar-val">O(n log n)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">WORST</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:90%;background:var(--accent)"></div></div><span class="sc-bar-val">O(n log n)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">STABLE</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:10%;background:var(--accent2)"></div></div><span class="sc-bar-val">NO</span></div>
      </div>
    </div>
    <div class="speed-card fast">
      <div class="sc-name">Merge Sort</div>
      <div class="sc-used">Used in: Stable sort, linked lists, external sorting</div>
      <div class="sc-bars">
        <div class="sc-bar-row"><span class="sc-bar-label">BEST</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:88%;background:var(--green)"></div></div><span class="sc-bar-val">O(n log n)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">AVG</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:85%;background:var(--green)"></div></div><span class="sc-bar-val">O(n log n)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">WORST</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:82%;background:var(--green)"></div></div><span class="sc-bar-val">O(n log n)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">STABLE</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:100%;background:var(--green)"></div></div><span class="sc-bar-val">YES</span></div>
      </div>
    </div>
    <div class="speed-card fast">
      <div class="sc-name">Quick Sort</div>
      <div class="sc-used">Used in: Cache-efficient in-place sorting, general purpose</div>
      <div class="sc-bars">
        <div class="sc-bar-row"><span class="sc-bar-label">BEST</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:92%;background:var(--green)"></div></div><span class="sc-bar-val">O(n log n)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">AVG</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:88%;background:var(--green)"></div></div><span class="sc-bar-val">O(n log n)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">WORST</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:30%;background:var(--accent2)"></div></div><span class="sc-bar-val">O(n^2) WARN</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">STABLE</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:10%;background:var(--accent2)"></div></div><span class="sc-bar-val">NO</span></div>
      </div>
    </div>
    <div class="speed-card fast">
      <div class="sc-name">Radix Sort</div>
      <div class="sc-used">Used in: Suffix arrays, integer keys, databases</div>
      <div class="sc-bars">
        <div class="sc-bar-row"><span class="sc-bar-label">BEST</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:95%;background:var(--green)"></div></div><span class="sc-bar-val">O(nk)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">AVG</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:90%;background:var(--green)"></div></div><span class="sc-bar-val">O(nk)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">WORST</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:88%;background:var(--green)"></div></div><span class="sc-bar-val">O(nk)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">STABLE</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:100%;background:var(--green)"></div></div><span class="sc-bar-val">YES</span></div>
      </div>
    </div>
    <div class="speed-card med">
      <div class="sc-name">Comb Sort</div>
      <div class="sc-used">Used in: Improved bubble -- shrink factor removes slow elements early</div>
      <div class="sc-bars">
        <div class="sc-bar-row"><span class="sc-bar-label">BEST</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:70%;background:var(--accent3)"></div></div><span class="sc-bar-val">O(n log n)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">AVG</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:52%;background:var(--accent3)"></div></div><span class="sc-bar-val">O(n^2/2^p)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">WORST</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:30%;background:var(--accent2)"></div></div><span class="sc-bar-val">O(n^2)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">STABLE</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:10%;background:var(--accent2)"></div></div><span class="sc-bar-val">NO</span></div>
      </div>
    </div>
    <div class="speed-card slow">
      <div class="sc-name">Bubble Sort</div>
      <div class="sc-used">Used in: Teaching only -- never use in production</div>
      <div class="sc-bars">
        <div class="sc-bar-row"><span class="sc-bar-label">BEST</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:50%;background:var(--accent3)"></div></div><span class="sc-bar-val">O(n)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">AVG</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:18%;background:var(--accent2)"></div></div><span class="sc-bar-val">O(n^2)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">WORST</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:15%;background:var(--accent2)"></div></div><span class="sc-bar-val">O(n^2)</span></div>
        <div class="sc-bar-row"><span class="sc-bar-label">STABLE</span><div class="sc-bar-track"><div class="sc-bar-fill" style="width:100%;background:var(--green)"></div></div><span class="sc-bar-val">YES</span></div>
      </div>
    </div>
  </div>
  <div style="padding:16px 18px;background:var(--panel);border:1px solid var(--border);border-radius:4px;font-size:12px;line-height:2;color:#7888aa;">
    <span style="color:var(--accent);font-family:'Bebas Neue',sans-serif;font-size:16px;letter-spacing:2px;">WHEN TO USE WHICH ALGORITHM</span><br>
    <span style="color:var(--text)">General purpose (unknown data):</span> Tim Sort -- adapts to real data patterns automatically.<br>
    <span style="color:var(--text)">Need in-place + no worst-case risk:</span> Intro Sort -- falls back to heap sort when quicksort recurses too deep.<br>
    <span style="color:var(--text)">Need stable sort (preserve equal-element order):</span> Merge Sort or Tim Sort.<br>
    <span style="color:var(--text)">Sorting integers with known range:</span> Radix Sort or Counting Sort -- can beat O(n log n).<br>
    <span style="color:var(--text)">Flash storage / minimize writes:</span> Cycle Sort -- fewest possible memory writes.<br>
    <span style="color:var(--text)">Nearly sorted data:</span> Insertion Sort or Tim Sort -- both are O(n) on sorted input.<br>
    <span style="color:var(--text)">Just learning:</span> Bubble then Insertion then Merge then Quick, in that order.
  </div>
</div>

<!-- TAB 3: PYTHON CODE -->
<div id="tab-pycode" class="tab-panel">
  <div class="code-panel">
    <h3>Python Implementations -- clean snake_case naming</h3>
    <div class="sub-tabs" id="py-tabs">
      <button class="btn real active" data-code="tim">Tim Sort</button>
      <button class="btn real" data-code="intro">Intro Sort</button>
      <button class="btn" data-code="merge">Merge</button>
      <button class="btn" data-code="quick">Quick</button>
      <button class="btn" data-code="heap">Heap</button>
      <button class="btn" data-code="comb">Comb</button>
      <button class="btn" data-code="cocktail">Cocktail</button>
      <button class="btn" data-code="shell">Shell</button>
      <button class="btn" data-code="cycle">Cycle</button>
      <button class="btn" data-code="counting">Counting</button>
      <button class="btn" data-code="radix">Radix</button>
      <button class="btn" data-code="bubble">Bubble</button>
      <button class="btn" data-code="insertion">Insertion</button>
    </div>
    <pre id="py-code"></pre>
  </div>
</div>

</div>
<script>
// TAB SWITCHING
document.querySelectorAll('.main-tab').forEach(t=>t.addEventListener('click',()=>{
  document.querySelectorAll('.main-tab').forEach(x=>x.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(x=>x.classList.remove('active'));
  t.classList.add('active');
  document.getElementById('tab-'+t.dataset.tab).classList.add('active');
  if(t.dataset.tab==='viz'){resize();draw();}
}));

const META={
  tim:     {name:'TIM SORT',       best:'O(n)',       avg:'O(n log n)',  worst:'O(n log n)',  space:'O(n)',    stable:'Yes', used:'Python, Java, Android',     desc:'Detects natural sorted runs, insertion-sorts small chunks, merge-sorts large ones. Dominates on real data.'},
  intro:   {name:'INTRO SORT',     best:'O(n log n)', avg:'O(n log n)',  worst:'O(n log n)',  space:'O(log n)',stable:'No',  used:'C++ std::sort, .NET, GNU',   desc:'Starts as quicksort, switches to heapsort if recursion goes too deep, and insertion sort for small sub-arrays.'},
  merge:   {name:'MERGE SORT',     best:'O(n log n)', avg:'O(n log n)',  worst:'O(n log n)',  space:'O(n)',    stable:'Yes', used:'Linked lists, stable sort',   desc:'Divides array in half, recursively sorts each half, then merges. Guaranteed O(n log n) and stable.'},
  quick:   {name:'QUICK SORT',     best:'O(n log n)', avg:'O(n log n)',  worst:'O(n^2)',      space:'O(log n)',stable:'No',  used:'General purpose, in-place',   desc:'Partitions around a pivot. Very cache-friendly. Worst case O(n^2) avoided with random pivot or median-of-three.'},
  heap:    {name:'HEAP SORT',      best:'O(n log n)', avg:'O(n log n)',  worst:'O(n log n)',  space:'O(1)',    stable:'No',  used:'Priority queues, embedded',   desc:'Builds max-heap then extracts. In-place with guaranteed O(n log n). Poor cache performance vs quicksort.'},
  comb:    {name:'COMB SORT',      best:'O(n log n)', avg:'O(n^2/2^p)', worst:'O(n^2)',      space:'O(1)',    stable:'No',  used:'Improved bubble alternative', desc:'Uses shrink factor ~1.3 to jump comparisons far apart, eliminating slow turtle elements early. Much faster than bubble.'},
  cocktail:{name:'COCKTAIL SHAKER',best:'O(n)',       avg:'O(n^2)',      worst:'O(n^2)',      space:'O(1)',    stable:'Yes', used:'Nearly-sorted data',          desc:'Bidirectional bubble sort -- passes alternate left-to-right then right-to-left. Better than bubble on partially sorted arrays.'},
  shell:   {name:'SHELL SORT',     best:'O(n log n)', avg:'O(n log^2 n)',worst:'O(n^2)',      space:'O(1)',    stable:'No',  used:'Embedded systems, small n',   desc:'Gap-based insertion sort. Ciura gap sequence gives best practical performance.'},
  cycle:   {name:'CYCLE SORT',     best:'O(n^2)',     avg:'O(n^2)',      worst:'O(n^2)',      space:'O(1)',    stable:'No',  used:'Flash memory, min-write',     desc:'Theoretically optimal for minimising the total number of writes to storage. Useful for flash/EEPROM.'},
  counting:{name:'COUNTING SORT',  best:'O(n+k)',     avg:'O(n+k)',      worst:'O(n+k)',      space:'O(k)',    stable:'Yes', used:'Small integer range',         desc:'Counts occurrences. Extremely fast when value range k is small. Degrades with large k.'},
  radix:   {name:'RADIX SORT',     best:'O(nk)',      avg:'O(nk)',       worst:'O(nk)',       space:'O(n+k)', stable:'Yes', used:'Strings, integers, DNA seq',   desc:'Sorts digit-by-digit. Achieves sub-O(n log n) on integers. LSD variant processes least-significant digit first.'},
  bubble:  {name:'BUBBLE SORT',    best:'O(n)',       avg:'O(n^2)',      worst:'O(n^2)',      space:'O(1)',    stable:'Yes', used:'Teaching only',               desc:'Repeatedly swaps adjacent out-of-order elements. Simple to understand but too slow for real use.'},
  insertion:{name:'INSERTION SORT',best:'O(n)',       avg:'O(n^2)',      worst:'O(n^2)',      space:'O(1)',    stable:'Yes', used:'Small n, nearly sorted',      desc:'Excellent for small arrays or nearly-sorted data. Used as the base case inside Tim Sort and Intro Sort.'},
  selection:{name:'SELECTION SORT',best:'O(n^2)',     avg:'O(n^2)',      worst:'O(n^2)',      space:'O(1)',    stable:'No',  used:'Teaching only',               desc:'Minimum number of swaps O(n), but too many comparisons. Only useful when write cost is extremely high.'},
  bogo:    {name:'BOGO SORT',      best:'O(n)',       avg:'O(n*n!)',     worst:'inf',         space:'O(1)',    stable:'No',  used:'Nowhere ever',                desc:'Random shuffle until sorted. Expected O(n*n!) comparisons. A joke. Do not use.'},
};

const PY={
tim:`<span class="cm"># Tim Sort -- Python's actual built-in algorithm (educational Python version)</span>
<span class="cm"># Real CPython uses optimised C. In Python just call: sorted(arr) or arr.sort()</span>
MIN_RUN = <span class="nm">32</span>

<span class="kw">def</span> <span class="fn">tim_sort</span>(input_array: list) -> list:
    <span class="st">"""Sort using Tim Sort: insertion sort small runs, merge them together."""</span>
    array_length = <span class="fn">len</span>(input_array)
    <span class="kw">for</span> run_start <span class="kw">in</span> <span class="fn">range</span>(<span class="nm">0</span>, array_length, MIN_RUN):
        run_end = <span class="fn">min</span>(run_start + MIN_RUN, array_length)
        <span class="fn">_insertion_sort_subarray</span>(input_array, run_start, run_end)
    current_size = MIN_RUN
    <span class="kw">while</span> current_size < array_length:
        <span class="kw">for</span> left_start <span class="kw">in</span> <span class="fn">range</span>(<span class="nm">0</span>, array_length, current_size * <span class="nm">2</span>):
            mid_point = <span class="fn">min</span>(left_start + current_size,     array_length)
            right_end = <span class="fn">min</span>(left_start + current_size * <span class="nm">2</span>, array_length)
            <span class="kw">if</span> mid_point < right_end:
                <span class="fn">_merge_into</span>(input_array, left_start, mid_point, right_end)
        current_size *= <span class="nm">2</span>
    <span class="kw">return</span> input_array

<span class="kw">def</span> <span class="fn">_insertion_sort_subarray</span>(array: list, start: int, end: int) -> <span class="bi">None</span>:
    <span class="kw">for</span> i <span class="kw">in</span> <span class="fn">range</span>(start + <span class="nm">1</span>, end):
        current_key, j = array[i], i - <span class="nm">1</span>
        <span class="kw">while</span> j >= start <span class="kw">and</span> array[j] > current_key:
            array[j + <span class="nm">1</span>] = array[j]; j -= <span class="nm">1</span>
        array[j + <span class="nm">1</span>] = current_key

<span class="kw">def</span> <span class="fn">_merge_into</span>(array: list, left: int, mid: int, right: int) -> <span class="bi">None</span>:
    left_buf  = array[left:mid]
    right_buf = array[mid:right]
    i = j = <span class="nm">0</span>; k = left
    <span class="kw">while</span> i < <span class="fn">len</span>(left_buf) <span class="kw">and</span> j < <span class="fn">len</span>(right_buf):
        <span class="kw">if</span> left_buf[i] <= right_buf[j]: array[k] = left_buf[i];  i += <span class="nm">1</span>
        <span class="kw">else</span>:                           array[k] = right_buf[j]; j += <span class="nm">1</span>
        k += <span class="nm">1</span>
    <span class="kw">while</span> i < <span class="fn">len</span>(left_buf):  array[k] = left_buf[i];  i += <span class="nm">1</span>; k += <span class="nm">1</span>
    <span class="kw">while</span> j < <span class="fn">len</span>(right_buf): array[k] = right_buf[j]; j += <span class="nm">1</span>; k += <span class="nm">1</span>`,

intro:`<span class="cm"># Intro Sort -- C++ std::sort strategy: Quick then Heap then Insertion</span>
<span class="kw">import</span> math
INSERTION_THRESHOLD = <span class="nm">16</span>

<span class="kw">def</span> <span class="fn">intro_sort</span>(input_array: list) -> list:
    <span class="st">"""Sort using Intro Sort: quicksort with heap-sort fallback."""</span>
    max_depth = <span class="nm">2</span> * <span class="fn">int</span>(math.<span class="fn">log2</span>(<span class="fn">len</span>(input_array))) <span class="kw">if</span> <span class="fn">len</span>(input_array) > <span class="nm">1</span> <span class="kw">else</span> <span class="nm">0</span>
    <span class="fn">_intro_recursive</span>(input_array, <span class="nm">0</span>, <span class="fn">len</span>(input_array) - <span class="nm">1</span>, max_depth)
    <span class="kw">return</span> input_array

<span class="kw">def</span> <span class="fn">_intro_recursive</span>(array: list, low: int, high: int, depth_limit: int) -> <span class="bi">None</span>:
    <span class="kw">if</span> high - low < INSERTION_THRESHOLD:
        <span class="fn">_insertion_range</span>(array, low, high); <span class="kw">return</span>
    <span class="kw">if</span> depth_limit == <span class="nm">0</span>:
        <span class="fn">_heap_range</span>(array, low, high); <span class="kw">return</span>
    pivot_idx = <span class="fn">_median_of_three</span>(array, low, high)
    array[pivot_idx], array[high] = array[high], array[pivot_idx]
    p = <span class="fn">_partition</span>(array, low, high)
    <span class="fn">_intro_recursive</span>(array, low,   p - <span class="nm">1</span>, depth_limit - <span class="nm">1</span>)
    <span class="fn">_intro_recursive</span>(array, p + <span class="nm">1</span>, high,  depth_limit - <span class="nm">1</span>)

<span class="kw">def</span> <span class="fn">_median_of_three</span>(array, low, high):
    mid = (low + high) // <span class="nm">2</span>
    candidates = [(array[low], low), (array[mid], mid), (array[high], high)]
    <span class="kw">return</span> <span class="fn">sorted</span>(candidates)[<span class="nm">1</span>][<span class="nm">1</span>]

<span class="kw">def</span> <span class="fn">_partition</span>(array, low, high):
    pivot, i = array[high], low - <span class="nm">1</span>
    <span class="kw">for</span> j <span class="kw">in</span> <span class="fn">range</span>(low, high):
        <span class="kw">if</span> array[j] <= pivot: i += <span class="nm">1</span>; array[i], array[j] = array[j], array[i]
    array[i+<span class="nm">1</span>], array[high] = array[high], array[i+<span class="nm">1</span>]; <span class="kw">return</span> i + <span class="nm">1</span>

<span class="kw">def</span> <span class="fn">_insertion_range</span>(array, low, high):
    <span class="kw">for</span> i <span class="kw">in</span> <span class="fn">range</span>(low+<span class="nm">1</span>, high+<span class="nm">1</span>):
        key, j = array[i], i-<span class="nm">1</span>
        <span class="kw">while</span> j >= low <span class="kw">and</span> array[j] > key: array[j+<span class="nm">1</span>]=array[j]; j-=<span class="nm">1</span>
        array[j+<span class="nm">1</span>] = key

<span class="kw">def</span> <span class="fn">_heap_range</span>(array, low, high):
    sub = array[low:high+<span class="nm">1</span>]; n = <span class="fn">len</span>(sub)
    <span class="kw">for</span> i <span class="kw">in</span> <span class="fn">range</span>(n//<span class="nm">2</span>-<span class="nm">1</span>,-<span class="nm">1</span>,-<span class="nm">1</span>): <span class="fn">_hfy</span>(sub,n,i)
    <span class="kw">for</span> i <span class="kw">in</span> <span class="fn">range</span>(n-<span class="nm">1</span>,<span class="nm">0</span>,-<span class="nm">1</span>): sub[<span class="nm">0</span>],sub[i]=sub[i],sub[<span class="nm">0</span>]; <span class="fn">_hfy</span>(sub,i,<span class="nm">0</span>)
    array[low:high+<span class="nm">1</span>] = sub

<span class="kw">def</span> <span class="fn">_hfy</span>(a,n,i):
    lg,l,r=i,<span class="nm">2</span>*i+<span class="nm">1</span>,<span class="nm">2</span>*i+<span class="nm">2</span>
    <span class="kw">if</span> l<n <span class="kw">and</span> a[l]>a[lg]: lg=l
    <span class="kw">if</span> r<n <span class="kw">and</span> a[r]>a[lg]: lg=r
    <span class="kw">if</span> lg!=i: a[i],a[lg]=a[lg],a[i]; <span class="fn">_hfy</span>(a,n,lg)`,

comb:`<span class="cm"># Comb Sort -- improved Bubble Sort using shrink factor 1.3</span>
<span class="cm"># Eliminates slow turtle elements near the end of the array</span>
SHRINK_FACTOR = <span class="nm">1.3</span>

<span class="kw">def</span> <span class="fn">comb_sort</span>(input_array: list) -> list:
    <span class="st">"""Sort using comb sort -- much faster than bubble sort in practice."""</span>
    array_length = <span class="fn">len</span>(input_array)
    current_gap  = array_length
    is_sorted    = <span class="bi">False</span>
    <span class="kw">while not</span> is_sorted:
        current_gap = <span class="fn">int</span>(current_gap / SHRINK_FACTOR)
        <span class="kw">if</span> current_gap <= <span class="nm">1</span>:
            current_gap = <span class="nm">1</span>
            is_sorted   = <span class="bi">True</span>
        index = <span class="nm">0</span>
        <span class="kw">while</span> index + current_gap < array_length:
            <span class="kw">if</span> input_array[index] > input_array[index + current_gap]:
                input_array[index], input_array[index + current_gap] = (
                    input_array[index + current_gap], input_array[index])
                is_sorted = <span class="bi">False</span>
            index += <span class="nm">1</span>
    <span class="kw">return</span> input_array`,

cocktail:`<span class="cm"># Cocktail Shaker Sort -- bidirectional Bubble Sort</span>
<span class="kw">def</span> <span class="fn">cocktail_shaker_sort</span>(input_array: list) -> list:
    <span class="st">"""Sort bidirectionally -- better than bubble on nearly-sorted data."""</span>
    left_boundary  = <span class="nm">0</span>
    right_boundary = <span class="fn">len</span>(input_array) - <span class="nm">1</span>
    <span class="kw">while</span> left_boundary < right_boundary:
        last_swap = left_boundary
        <span class="kw">for</span> i <span class="kw">in</span> <span class="fn">range</span>(left_boundary, right_boundary):
            <span class="kw">if</span> input_array[i] > input_array[i + <span class="nm">1</span>]:
                input_array[i], input_array[i+<span class="nm">1</span>] = input_array[i+<span class="nm">1</span>], input_array[i]
                last_swap = i
        right_boundary = last_swap
        <span class="kw">for</span> i <span class="kw">in</span> <span class="fn">range</span>(right_boundary, left_boundary, -<span class="nm">1</span>):
            <span class="kw">if</span> input_array[i] < input_array[i - <span class="nm">1</span>]:
                input_array[i], input_array[i-<span class="nm">1</span>] = input_array[i-<span class="nm">1</span>], input_array[i]
                last_swap = i
        left_boundary = last_swap
    <span class="kw">return</span> input_array`,

cycle:`<span class="cm"># Cycle Sort -- minimises total number of writes (for flash memory)</span>
<span class="kw">def</span> <span class="fn">cycle_sort</span>(input_array: list) -> list:
    <span class="st">"""Sort with the absolute minimum number of array writes."""</span>
    array_length = <span class="fn">len</span>(input_array)
    <span class="kw">for</span> cycle_start <span class="kw">in</span> <span class="fn">range</span>(array_length - <span class="nm">1</span>):
        element_to_place = input_array[cycle_start]
        correct_position = cycle_start
        <span class="kw">for</span> scan_index <span class="kw">in</span> <span class="fn">range</span>(cycle_start + <span class="nm">1</span>, array_length):
            <span class="kw">if</span> input_array[scan_index] < element_to_place:
                correct_position += <span class="nm">1</span>
        <span class="kw">if</span> correct_position == cycle_start:
            <span class="kw">continue</span>
        <span class="kw">while</span> element_to_place == input_array[correct_position]:
            correct_position += <span class="nm">1</span>
        input_array[correct_position], element_to_place = element_to_place, input_array[correct_position]
        <span class="kw">while</span> correct_position != cycle_start:
            correct_position = cycle_start
            <span class="kw">for</span> scan_index <span class="kw">in</span> <span class="fn">range</span>(cycle_start + <span class="nm">1</span>, array_length):
                <span class="kw">if</span> input_array[scan_index] < element_to_place:
                    correct_position += <span class="nm">1</span>
            <span class="kw">while</span> element_to_place == input_array[correct_position]:
                correct_position += <span class="nm">1</span>
            input_array[correct_position], element_to_place = element_to_place, input_array[correct_position]
    <span class="kw">return</span> input_array`,

shell:`<span class="cm"># Shell Sort using Ciura gap sequence (best known practical gap sequence)</span>
CIURA_GAPS = [<span class="nm">701</span>, <span class="nm">301</span>, <span class="nm">132</span>, <span class="nm">57</span>, <span class="nm">23</span>, <span class="nm">10</span>, <span class="nm">4</span>, <span class="nm">1</span>]

<span class="kw">def</span> <span class="fn">shell_sort</span>(input_array: list) -> list:
    <span class="st">"""Sort using Shell sort with Ciura gap sequence."""</span>
    array_length = <span class="fn">len</span>(input_array)
    <span class="kw">for</span> gap_size <span class="kw">in</span> CIURA_GAPS:
        <span class="kw">if</span> gap_size >= array_length: <span class="kw">continue</span>
        <span class="kw">for</span> i <span class="kw">in</span> <span class="fn">range</span>(gap_size, array_length):
            element_to_insert, j = input_array[i], i
            <span class="kw">while</span> j >= gap_size <span class="kw">and</span> input_array[j - gap_size] > element_to_insert:
                input_array[j] = input_array[j - gap_size]; j -= gap_size
            input_array[j] = element_to_insert
    <span class="kw">return</span> input_array`,

merge:`<span class="cm"># Merge Sort -- O(n log n) guaranteed, stable</span>
<span class="kw">def</span> <span class="fn">merge_sort</span>(input_array: list) -> list:
    <span class="st">"""Recursively split and merge sorted halves."""</span>
    <span class="kw">if</span> <span class="fn">len</span>(input_array) <= <span class="nm">1</span>: <span class="kw">return</span> input_array
    mid        = <span class="fn">len</span>(input_array) // <span class="nm">2</span>
    left_half  = <span class="fn">merge_sort</span>(input_array[:mid])
    right_half = <span class="fn">merge_sort</span>(input_array[mid:])
    return <span class="fn">_merge_halves</span>(left_half, right_half)

<span class="kw">def</span> <span class="fn">_merge_halves</span>(left_array: list, right_array: list) -> list:
    merged, i, j = [], <span class="nm">0</span>, <span class="nm">0</span>
    <span class="kw">while</span> i < <span class="fn">len</span>(left_array) <span class="kw">and</span> j < <span class="fn">len</span>(right_array):
        <span class="kw">if</span> left_array[i] <= right_array[j]: merged.<span class="fn">append</span>(left_array[i]);  i += <span class="nm">1</span>
        <span class="kw">else</span>:                               merged.<span class="fn">append</span>(right_array[j]); j += <span class="nm">1</span>
    <span class="kw">return</span> merged + left_array[i:] + right_array[j:]`,

quick:`<span class="cm"># Quick Sort -- O(n log n) average, in-place, cache-friendly</span>
<span class="kw">def</span> <span class="fn">quick_sort</span>(input_array: list, low: int = <span class="nm">0</span>, high: int = <span class="bi">None</span>) -> list:
    <span class="st">"""Sort by partitioning around a pivot element recursively."""</span>
    <span class="kw">if</span> high <span class="kw">is</span> <span class="bi">None</span>: high = <span class="fn">len</span>(input_array) - <span class="nm">1</span>
    <span class="kw">if</span> low < high:
        pivot_pos = <span class="fn">_partition_pivot</span>(input_array, low, high)
        <span class="fn">quick_sort</span>(input_array, low, pivot_pos - <span class="nm">1</span>)
        <span class="fn">quick_sort</span>(input_array, pivot_pos + <span class="nm">1</span>, high)
    <span class="kw">return</span> input_array

<span class="kw">def</span> <span class="fn">_partition_pivot</span>(array, low, high):
    pivot, i = array[high], low - <span class="nm">1</span>
    <span class="kw">for</span> j <span class="kw">in</span> <span class="fn">range</span>(low, high):
        <span class="kw">if</span> array[j] < pivot:
            i += <span class="nm">1</span>; array[i], array[j] = array[j], array[i]
    array[i+<span class="nm">1</span>], array[high] = array[high], array[i+<span class="nm">1</span>]; <span class="kw">return</span> i + <span class="nm">1</span>`,

heap:`<span class="cm"># Heap Sort -- guaranteed O(n log n), in-place</span>
<span class="kw">def</span> <span class="fn">heap_sort</span>(input_array: list) -> list:
    <span class="st">"""Build max-heap then extract elements in sorted order."""</span>
    n = <span class="fn">len</span>(input_array)
    <span class="kw">for</span> i <span class="kw">in</span> <span class="fn">range</span>(n//<span class="nm">2</span>-<span class="nm">1</span>, -<span class="nm">1</span>, -<span class="nm">1</span>): <span class="fn">_heapify</span>(input_array, n, i)
    <span class="kw">for</span> i <span class="kw">in</span> <span class="fn">range</span>(n-<span class="nm">1</span>, <span class="nm">0</span>, -<span class="nm">1</span>):
        input_array[<span class="nm">0</span>], input_array[i] = input_array[i], input_array[<span class="nm">0</span>]
        <span class="fn">_heapify</span>(input_array, i, <span class="nm">0</span>)
    <span class="kw">return</span> input_array

<span class="kw">def</span> <span class="fn">_heapify</span>(array, heap_size, root):
    lg, l, r = root, <span class="nm">2</span>*root+<span class="nm">1</span>, <span class="nm">2</span>*root+<span class="nm">2</span>
    <span class="kw">if</span> l < heap_size <span class="kw">and</span> array[l] > array[lg]: lg = l
    <span class="kw">if</span> r < heap_size <span class="kw">and</span> array[r] > array[lg]: lg = r
    <span class="kw">if</span> lg != root:
        array[root], array[lg] = array[lg], array[root]
        <span class="fn">_heapify</span>(array, heap_size, lg)`,

counting:`<span class="cm"># Counting Sort -- O(n+k), only for non-negative integers</span>
<span class="kw">def</span> <span class="fn">counting_sort</span>(input_array: list) -> list:
    <span class="st">"""Sort by counting occurrences of each integer value."""</span>
    <span class="kw">if not</span> input_array: <span class="kw">return</span> input_array
    max_value        = <span class="fn">max</span>(input_array)
    occurrence_count = [<span class="nm">0</span>] * (max_value + <span class="nm">1</span>)
    <span class="kw">for</span> value <span class="kw">in</span> input_array: occurrence_count[value] += <span class="nm">1</span>
    write_index = <span class="nm">0</span>
    <span class="kw">for</span> value, count <span class="kw">in</span> <span class="fn">enumerate</span>(occurrence_count):
        <span class="kw">for</span> _ <span class="kw">in</span> <span class="fn">range</span>(count):
            input_array[write_index] = value; write_index += <span class="nm">1</span>
    <span class="kw">return</span> input_array`,

radix:`<span class="cm"># Radix Sort (LSD) -- O(nk), beats O(n log n) for integer keys</span>
<span class="kw">def</span> <span class="fn">radix_sort</span>(input_array: list) -> list:
    <span class="st">"""Sort integers digit-by-digit from least to most significant."""</span>
    <span class="kw">if not</span> input_array: <span class="kw">return</span> input_array
    max_value       = <span class="fn">max</span>(input_array)
    digit_exponent  = <span class="nm">1</span>
    <span class="kw">while</span> max_value // digit_exponent > <span class="nm">0</span>:
        input_array    = <span class="fn">_counting_pass</span>(input_array, digit_exponent)
        digit_exponent *= <span class="nm">10</span>
    <span class="kw">return</span> input_array

<span class="kw">def</span> <span class="fn">_counting_pass</span>(input_array, digit_exponent):
    n = <span class="fn">len</span>(input_array); output = [<span class="nm">0</span>]*n; count = [<span class="nm">0</span>]*<span class="nm">10</span>
    <span class="kw">for</span> v <span class="kw">in</span> input_array: count[(v//digit_exponent)%<span class="nm">10</span>] += <span class="nm">1</span>
    <span class="kw">for</span> i <span class="kw">in</span> <span class="fn">range</span>(<span class="nm">1</span>,<span class="nm">10</span>): count[i] += count[i-<span class="nm">1</span>]
    <span class="kw">for</span> v <span class="kw">in</span> <span class="fn">reversed</span>(input_array):
        d=(v//digit_exponent)%<span class="nm">10</span>; output[count[d]-<span class="nm">1</span>]=v; count[d]-=<span class="nm">1</span>
    <span class="kw">return</span> output`,

bubble:`<span class="cm"># Bubble Sort -- educational only, O(n^2)</span>
<span class="kw">def</span> <span class="fn">bubble_sort</span>(input_array: list) -> list:
    n = <span class="fn">len</span>(input_array)
    <span class="kw">for</span> i <span class="kw">in</span> <span class="fn">range</span>(n-<span class="nm">1</span>):
        swapped = <span class="bi">False</span>
        <span class="kw">for</span> j <span class="kw">in</span> <span class="fn">range</span>(n-i-<span class="nm">1</span>):
            <span class="kw">if</span> input_array[j] > input_array[j+<span class="nm">1</span>]:
                input_array[j], input_array[j+<span class="nm">1</span>] = input_array[j+<span class="nm">1</span>], input_array[j]
                swapped = <span class="bi">True</span>
        <span class="kw">if not</span> swapped: <span class="kw">break</span>
    <span class="kw">return</span> input_array`,

insertion:`<span class="cm"># Insertion Sort -- O(n) on nearly-sorted, base case inside Tim+Intro Sort</span>
<span class="kw">def</span> <span class="fn">insertion_sort</span>(input_array: list) -> list:
    <span class="kw">for</span> i <span class="kw">in</span> <span class="fn">range</span>(<span class="nm">1</span>, <span class="fn">len</span>(input_array)):
        current_element, j = input_array[i], i - <span class="nm">1</span>
        <span class="kw">while</span> j >= <span class="nm">0</span> <span class="kw">and</span> input_array[j] > current_element:
            input_array[j+<span class="nm">1</span>] = input_array[j]; j -= <span class="nm">1</span>
        input_array[j+<span class="nm">1</span>] = current_element
    <span class="kw">return</span> input_array`,
};

// CANVAS
const canvas=document.getElementById('cv'),ctx=canvas.getContext('2d');
let W,H;
const C={DEF:'#1e2545',ACTIVE:'#00f5d4',CMP:'#f72585',SORTED:'#3dff6e',PIVOT:'#fee440',RUN:'#7b2fff'};
let arr=[],colors=[],N=80,sorting=false,stop_flag=false,cmp_count=0,swp_count=0;

function resize(){
  const dpr=devicePixelRatio||1,r=canvas.getBoundingClientRect();
  W=r.width;H=r.height;canvas.width=W*dpr;canvas.height=H*dpr;ctx.scale(dpr,dpr);draw();
}
function draw(){
  ctx.clearRect(0,0,W,H);if(!arr.length)return;
  const gap=1,bw=(W-gap*(N-1))/N,mx=Math.max(...arr);
  for(let i=0;i<N;i++){
    const x=i*(bw+gap),bh=(arr[i]/mx)*(H-4),y=H-bh,col=colors[i]||C.DEF;
    ctx.shadowBlur=col!==C.DEF?10:0;ctx.shadowColor=col;ctx.fillStyle=col;
    ctx.beginPath();ctx.roundRect(x,y,Math.max(bw-0.5,1),bh,bw>5?[2,2,0,0]:0);ctx.fill();
  }ctx.shadowBlur=0;
}
function gen(){
  if(sorting)return;
  arr=Array.from({length:N},()=>Math.floor(Math.random()*(H-20))+10);
  colors=new Array(N).fill(C.DEF);cmp_count=swp_count=0;upd();prog(0);
  tick('// Array randomized -- SPACE to sort','');draw();
}
function upd(t){
  document.getElementById('s-cmp').textContent=cmp_count.toLocaleString();
  document.getElementById('s-swp').textContent=swp_count.toLocaleString();
  if(t!==undefined)document.getElementById('s-time').textContent=t;
}
function prog(p){document.getElementById('pf').style.width=p+'%';}
function tick(m,c){const e=document.getElementById('ticker');e.textContent=m;e.className='ticker '+(c||'');}
function delay(){const v=+document.getElementById('sp-sl').value;return Math.round((1-(v-1)/99)*130);}
const ms=d=>new Promise(r=>setTimeout(r,d));
async function step(){if(stop_flag)throw 0;cmp_count++;upd();draw();const d=delay();if(d>0)await ms(d);}
async function swp(i,j){swp_count++;[arr[i],arr[j]]=[arr[j],arr[i]];}

// Tim Sort
async function run_tim_sort(){
  const RUN=32;
  for(let s=0;s<N;s+=RUN){
    const e=Math.min(s+RUN,N);
    for(let i=s;i<e;i++)colors[i]=C.RUN;
    await ms(delay()*2);
    for(let i=s+1;i<e;i++){
      const key=arr[i];let j=i-1;colors[i]=C.ACTIVE;
      while(j>=s&&arr[j]>key){colors[j]=C.CMP;arr[j+1]=arr[j];swp_count++;colors[j+1]=C.DEF;j--;cmp_count++;upd();draw();const d=delay();if(d>0)await ms(d);if(stop_flag)throw 0;colors[j+1]=C.DEF;}
      arr[j+1]=key;for(let k=s;k<e;k++)colors[k]=C.SORTED;
    }
    prog((s+RUN)/N*60);
  }
  for(let size=RUN;size<N;size*=2){
    for(let l=0;l<N;l+=size*2){
      const m=Math.min(l+size,N),r=Math.min(l+size*2,N);
      if(m<r)await _tm(l,m,r);
    }
    prog(60+size/N*40);
  }
  mark_sorted();
}
async function _tm(l,m,r){
  const L=arr.slice(l,m),R=arr.slice(m,r);let i=0,j=0,k=l;
  while(i<L.length&&j<R.length){
    colors[k]=C.ACTIVE;cmp_count++;
    arr[k++]=L[i]<=R[j]?L[i++]:(swp_count++,R[j++]);
    upd();draw();const d=delay();if(d>0)await ms(Math.floor(d/2));if(stop_flag)throw 0;
  }
  while(i<L.length){arr[k++]=L[i++];swp_count++;draw();}
  while(j<R.length){arr[k++]=R[j++];swp_count++;draw();}
  for(let x=l;x<r;x++)colors[x]=C.SORTED;
}

// Intro Sort
async function run_intro_sort(){
  const max_depth=2*Math.floor(Math.log2(N));
  await _ir(0,N-1,max_depth);mark_sorted();
}
async function _ir(lo,hi,depth){
  if(stop_flag)throw 0;if(lo>=hi)return;
  if(hi-lo<16){await _vi(lo,hi);return;}
  if(depth===0){await _vh(lo,hi);return;}
  const p=await _vp(lo,hi);colors[p]=C.SORTED;
  await _ir(lo,p-1,depth-1);await _ir(p+1,hi,depth-1);
}

// Comb Sort
async function run_comb_sort(){
  let gap=N,sorted=false;
  while(!sorted){
    gap=Math.max(1,Math.floor(gap/1.3));sorted=(gap===1);
    for(let i=0;i+gap<N;i++){
      colors[i]=C.ACTIVE;colors[i+gap]=C.CMP;await step();
      if(arr[i]>arr[i+gap]){await swp(i,i+gap);sorted=false;}
      colors[i]=C.DEF;colors[i+gap]=C.DEF;
    }
    prog((1-gap/N)*100);
  }
  mark_sorted();
}

// Cocktail Shaker
async function run_cocktail_sort(){
  let lo=0,hi=N-1;
  while(lo<hi){
    let last=lo;
    for(let i=lo;i<hi;i++){colors[i]=C.ACTIVE;colors[i+1]=C.CMP;await step();if(arr[i]>arr[i+1]){await swp(i,i+1);last=i;}colors[i]=C.DEF;colors[i+1]=C.DEF;}
    colors[hi]=C.SORTED;hi=last;
    for(let i=hi;i>lo;i--){colors[i]=C.CMP;colors[i-1]=C.ACTIVE;await step();if(arr[i]<arr[i-1]){await swp(i,i-1);last=i;}colors[i]=C.DEF;colors[i-1]=C.DEF;}
    colors[lo]=C.SORTED;lo=last;
    prog((lo+N-hi)/N*100);
  }
  mark_sorted();
}

// Cycle Sort
async function run_cycle_sort(){
  for(let cs=0;cs<N-1;cs++){
    let item=arr[cs],pos=cs;colors[cs]=C.PIVOT;
    for(let i=cs+1;i<N;i++){colors[i]=C.CMP;cmp_count++;upd();draw();const d=delay();if(d>0)await ms(Math.floor(d/2));if(stop_flag)throw 0;if(arr[i]<item)pos++;colors[i]=C.DEF;}
    if(pos===cs){colors[cs]=C.SORTED;continue;}
    while(item===arr[pos])pos++;
    [arr[pos],item]=[item,arr[pos]];swp_count++;colors[pos]=C.ACTIVE;draw();await ms(delay());
    while(pos!==cs){
      pos=cs;
      for(let i=cs+1;i<N;i++){if(arr[i]<item)pos++;}
      while(item===arr[pos])pos++;
      [arr[pos],item]=[item,arr[pos]];swp_count++;colors[pos]=C.ACTIVE;draw();
      const d=delay();if(d>0)await ms(d);if(stop_flag)throw 0;
    }
    colors[cs]=C.SORTED;prog(cs/N*100);
  }
  mark_sorted();
}

// Shared helpers
async function _vi(lo,hi){
  for(let i=lo+1;i<=hi;i++){
    const key=arr[i];let j=i-1;colors[i]=C.ACTIVE;await step();
    while(j>=lo&&arr[j]>key){arr[j+1]=arr[j];swp_count++;colors[j+1]=C.DEF;j--;cmp_count++;upd();draw();const d=delay();if(d>0)await ms(d);if(stop_flag)throw 0;}
    arr[j+1]=key;for(let k=lo;k<=i;k++)colors[k]=C.SORTED;
  }
}
async function _vh(lo,hi){
  const n=hi-lo+1;
  for(let i=Math.floor(n/2)-1;i>=0;i--)await _hv(lo,hi,lo+i,n);
  for(let i=hi;i>lo;i--){
    colors[lo]=C.ACTIVE;colors[i]=C.CMP;await swp(lo,i);swp_count--;
    colors[i]=C.SORTED;colors[lo]=C.DEF;cmp_count++;upd();draw();
    const d=delay();if(d>0)await ms(d);if(stop_flag)throw 0;
    await _hv(lo,i-1,lo,i-lo);
  }
}
async function _hv(lo,hi,root,n){
  const i=root-lo;let lg=i,l=2*i+1,r=2*i+2;
  if(l<n&&arr[lo+l]>arr[lo+lg])lg=l;if(r<n&&arr[lo+r]>arr[lo+lg])lg=r;
  if(lg!==i){colors[lo+i]=C.CMP;colors[lo+lg]=C.ACTIVE;await swp(lo+i,lo+lg);swp_count--;cmp_count++;upd();draw();const d=delay();if(d>0)await ms(Math.floor(d/2));if(stop_flag)throw 0;colors[lo+i]=C.DEF;colors[lo+lg]=C.DEF;await _hv(lo,hi,lo+lg,n);}
}
async function _vp(lo,hi){
  const pv=arr[hi];colors[hi]=C.PIVOT;let i=lo-1;
  for(let j=lo;j<hi;j++){colors[j]=C.CMP;cmp_count++;if(arr[j]<pv){i++;await swp(i,j);colors[i]=C.ACTIVE;colors[j]=C.DEF;}else colors[j]=C.DEF;upd();draw();const d=delay();if(d>0)await ms(d);if(stop_flag)throw 0;}
  await swp(i+1,hi);colors[hi]=C.DEF;return i+1;
}

// Classic algorithms
async function run_merge_sort(){await _ms(0,N-1);mark_sorted();}
async function _ms(l,r){if(stop_flag)throw 0;if(l>=r)return;const m=(l+r)>>1;await _ms(l,m);await _ms(m+1,r);await _tm(l,m+1,r+1);}
async function run_quick_sort(){await _qs(0,N-1);mark_sorted();}
async function _qs(lo,hi){if(stop_flag)throw 0;if(lo>=hi)return;const p=await _vp(lo,hi);colors[p]=C.SORTED;await _qs(lo,p-1);await _qs(p+1,hi);}
async function run_heap_sort(){for(let i=Math.floor(N/2)-1;i>=0;i--)await _hv(0,N-1,i,N);for(let i=N-1;i>0;i--){colors[0]=C.ACTIVE;colors[i]=C.CMP;await swp(0,i);colors[i]=C.SORTED;colors[0]=C.DEF;cmp_count++;upd();draw();const d=delay();if(d>0)await ms(d);if(stop_flag)throw 0;await _hv(0,i-1,0,i);}mark_sorted();}
async function run_shell_sort(){
  const gaps=[701,301,132,57,23,10,4,1];
  for(const gap of gaps){if(gap>=N)continue;
    for(let i=gap;i<N;i++){const key=arr[i];let j=i;colors[i]=C.ACTIVE;
      while(j>=gap&&arr[j-gap]>key){colors[j-gap]=C.CMP;arr[j]=arr[j-gap];swp_count++;colors[j]=C.DEF;j-=gap;cmp_count++;upd();draw();const d=delay();if(d>0)await ms(d);if(stop_flag)throw 0;colors[j]=C.DEF;}
      arr[j]=key;colors[j]=C.SORTED;}prog(100-gap/N*100);}
  mark_sorted();}
async function run_counting_sort(){
  const mx=Math.max(...arr),cnt=new Array(mx+1).fill(0);
  for(const v of arr){cnt[v]++;cmp_count++;}let wi=0;
  for(let v=0;v<=mx;v++)for(let c=0;c<cnt[v];c++){arr[wi]=v;colors[wi]=C.ACTIVE;swp_count++;upd();draw();const d=delay();if(d>0)await ms(d);if(stop_flag)throw 0;colors[wi]=C.SORTED;wi++;prog(wi/N*100);}
  mark_sorted();}
async function run_radix_sort(){
  const mx=Math.max(...arr);
  for(let e=1;Math.floor(mx/e)>0;e*=10){
    const out=new Array(N).fill(0),cnt=new Array(10).fill(0);
    for(const v of arr)cnt[Math.floor(v/e)%10]++;
    for(let i=1;i<10;i++)cnt[i]+=cnt[i-1];
    for(let i=N-1;i>=0;i--){const d=Math.floor(arr[i]/e)%10;out[cnt[d]-1]=arr[i];cnt[d]--;}
    for(let i=0;i<N;i++){arr[i]=out[i];colors[i]=C.ACTIVE;swp_count++;cmp_count++;upd();draw();const d=delay();if(d>0)await ms(Math.floor(d/2));if(stop_flag)throw 0;colors[i]=C.DEF;prog((i+1)/N*100);}
  }mark_sorted();}
async function run_bubble_sort(){
  for(let i=0;i<N-1;i++){let s=false;for(let j=0;j<N-i-1;j++){colors[j]=C.ACTIVE;colors[j+1]=C.CMP;await step();if(arr[j]>arr[j+1]){await swp(j,j+1);s=true;}colors[j]=C.DEF;colors[j+1]=C.DEF;}colors[N-1-i]=C.SORTED;prog((i+1)/(N-1)*100);if(!s)break;}mark_sorted();}
async function run_selection_sort(){
  for(let i=0;i<N-1;i++){let mi=i;colors[i]=C.ACTIVE;for(let j=i+1;j<N;j++){colors[j]=C.CMP;await step();if(arr[j]<arr[mi]){if(mi!==i)colors[mi]=C.DEF;mi=j;colors[mi]=C.PIVOT;}else colors[j]=C.DEF;}if(mi!==i)await swp(i,mi);colors[i]=C.SORTED;colors[mi]=C.DEF;prog((i+1)/(N-1)*100);}mark_sorted();}
async function run_insertion_sort(){
  colors[0]=C.SORTED;
  for(let i=1;i<N;i++){const key=arr[i];let j=i-1;colors[i]=C.ACTIVE;await step();while(j>=0&&arr[j]>key){colors[j]=C.CMP;arr[j+1]=arr[j];swp_count++;colors[j+1]=C.DEF;j--;cmp_count++;upd();draw();const d=delay();if(d>0)await ms(d);if(stop_flag)throw 0;}arr[j+1]=key;for(let k=0;k<=i;k++)colors[k]=C.SORTED;prog((i+1)/N*100);}mark_sorted();}
async function run_bogo_sort(){
  const ok=()=>{for(let i=0;i<N-1;i++)if(arr[i]>arr[i+1])return false;return true;};
  const sh=()=>{for(let i=N-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[arr[i],arr[j]]=[arr[j],arr[i]];swp_count++;}};
  let t=0;while(!ok()){cmp_count+=N;sh();t++;tick('// Bogo Sort attempt #'+t.toLocaleString()+' -- good luck!','on');upd();draw();await ms(Math.max(12,delay()));if(stop_flag)throw 0;if(t>2000){tick('// Bogo gave up at 2000 attempts','on');break;}}mark_sorted();}

function mark_sorted(){colors=new Array(N).fill(C.SORTED);prog(100);draw();}
async function sweep(){const d=Math.max(1,Math.floor(260/N));for(let i=0;i<N;i++){colors[i]='#ffffff';draw();await ms(d);colors[i]=C.SORTED;}draw();}

// Orchestrate
let selected_algo='tim';
async function start_sort(){
  if(sorting)return;sorting=true;stop_flag=false;cmp_count=swp_count=0;
  colors=new Array(N).fill(C.DEF);upd();prog(0);set_disabled(true);tick('// Sorting in progress...','on');
  const t0=performance.now();
  try{
    switch(selected_algo){
      case 'tim':      await run_tim_sort();      break;
      case 'intro':    await run_intro_sort();     break;
      case 'merge':    await run_merge_sort();     break;
      case 'quick':    await run_quick_sort();     break;
      case 'heap':     await run_heap_sort();      break;
      case 'comb':     await run_comb_sort();      break;
      case 'cocktail': await run_cocktail_sort();  break;
      case 'shell':    await run_shell_sort();     break;
      case 'cycle':    await run_cycle_sort();     break;
      case 'counting': await run_counting_sort();  break;
      case 'radix':    await run_radix_sort();     break;
      case 'bubble':   await run_bubble_sort();    break;
      case 'selection':await run_selection_sort(); break;
      case 'insertion':await run_insertion_sort(); break;
      case 'bogo':     await run_bogo_sort();      break;
    }
    const t=(performance.now()-t0).toFixed(1);upd(t+' ms');
    tick('// Done -- '+cmp_count.toLocaleString()+' comparisons, '+swp_count.toLocaleString()+' writes, '+t+'ms','ok');
    await sweep();
  }catch(e){colors=new Array(N).fill(C.DEF);draw();tick('// Stopped','');}
  sorting=false;set_disabled(false);
}
function set_disabled(on){
  ['btn-sort','btn-gen'].forEach(id=>document.getElementById(id).disabled=on);
  document.getElementById('btn-stop').disabled=!on;
  document.querySelectorAll('[data-algo]').forEach(b=>b.disabled=on);
}

// UI wiring
document.getElementById('btn-sort').addEventListener('click',start_sort);
document.getElementById('btn-gen').addEventListener('click',gen);
document.getElementById('btn-stop').addEventListener('click',()=>stop_flag=true);
document.getElementById('sz-sl').addEventListener('input',function(){N=+this.value;document.getElementById('sz-v').textContent=N;document.getElementById('s-sz').textContent=N;if(!sorting)gen();});
document.getElementById('sp-sl').addEventListener('input',function(){document.getElementById('sp-v').textContent=this.value;});
document.querySelectorAll('[data-algo]').forEach(btn=>btn.addEventListener('click',()=>{
  if(sorting)return;
  selected_algo=btn.dataset.algo;
  document.querySelectorAll('[data-algo]').forEach(b=>b.classList.remove('active'));btn.classList.add('active');
  const m=META[selected_algo]||{};
  ['a-disp','cx-name'].forEach(id=>document.getElementById(id).textContent=m.name||'');
  document.getElementById('cx-b').textContent=m.best||'';
  document.getElementById('cx-a').textContent=m.avg||'';
  document.getElementById('cx-w').textContent=m.worst||'';
  document.getElementById('cx-s').textContent=m.space||'';
  document.getElementById('cx-st').textContent=m.stable||'';
  document.getElementById('cx-u').textContent=m.used||'';
  document.getElementById('cx-d').textContent=m.desc||'';
  tick('// '+m.name+' selected -- press SORT or SPACE','');
  const ct=document.querySelector('[data-code="'+selected_algo+'"]');if(ct)ct.click();
}));
document.getElementById('py-tabs').addEventListener('click',e=>{
  const b=e.target.closest('[data-code]');if(!b)return;
  document.querySelectorAll('[data-code]').forEach(x=>x.classList.remove('active'));b.classList.add('active');
  document.getElementById('py-code').innerHTML=PY[b.dataset.code]||'<span style="color:var(--dim)">// see visualizer tab</span>';
});
document.addEventListener('keydown',e=>{
  if(e.code==='Space'){e.preventDefault();if(!sorting)start_sort();else stop_flag=true;}
  if(e.code==='KeyR'&&!sorting)gen();
});
window.addEventListener('resize',resize);
window.addEventListener('load',()=>{resize();gen();document.getElementById('py-code').innerHTML=PY['tim'];});
</script>
</body>
</html>'''


class SortVisualizerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = HTML.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type',   'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass  # suppress per-request logs


def open_browser(port):
    time.sleep(0.8)
    webbrowser.open('http://127.0.0.1:{}'.format(port))


def run_server(port=PORT):
    server = http.server.HTTPServer(('127.0.0.1', port), SortVisualizerHandler)
    print('')
    print('  +----------------------------------------------+')
    print('  |   SORT // VISUALIZER  --  15 Algorithms      |')
    print('  +----------------------------------------------+')
    print('  |   URL  ->  http://127.0.0.1:{}             |'.format(port))
    print('  |   Stop ->  Ctrl+C in this terminal           |')
    print('  +----------------------------------------------+')
    print('')
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  Server stopped. Goodbye!\n')
        server.shutdown()


if __name__ == '__main__':
    run_server()
