/**
 * deck-render.js — Canvas 2D deck renderer for Cockpitdecks
 *
 * Renders deck button grids (with annunciators, text, labels, side screens) onto an
 * HTML Canvas element.  Works in two modes:
 *
 *   Static (doc previews)
 *     const r = new DeckRenderer(canvas, DECK_CONFIG);
 *     r.showPage('index');
 *
 *   Live (web deck, Phase 2 — WebSocket image feed)
 *     const r = new DeckRenderer(canvas, DECK_CONFIG);
 *     r.setPng(keyIndex, base64PngDataUri);   // called per frame from WS handler
 *
 * DECK_CONFIG is a JSON object produced by yaml_to_json() in render_deck_preview.py.
 */

// ─── CSS color name table ────────────────────────────────────────────────────

const CSS_NAMED = {
  aliceblue:'#f0f8ff',antiquewhite:'#faebd7',aqua:'#00ffff',aquamarine:'#7fffd4',
  azure:'#f0ffff',beige:'#f5f5dc',bisque:'#ffe4c4',black:'#000000',
  blanchedalmond:'#ffebcd',blue:'#0000ff',blueviolet:'#8a2be2',brown:'#a52a2a',
  burlywood:'#deb887',cadetblue:'#5f9ea0',chartreuse:'#7fff00',chocolate:'#d2691e',
  coral:'#ff7f50',cornflowerblue:'#6495ed',cornsilk:'#fff8dc',crimson:'#dc143c',
  cyan:'#00ffff',darkblue:'#00008b',darkcyan:'#008b8b',darkgoldenrod:'#b8860b',
  darkgray:'#a9a9a9',darkgrey:'#a9a9a9',darkgreen:'#006400',darkkhaki:'#bdb76b',
  darkmagenta:'#8b008b',darkolivegreen:'#556b2f',darkorange:'#ff8c00',
  darkorchid:'#9932cc',darkred:'#8b0000',darksalmon:'#e9967a',darkseagreen:'#8fbc8f',
  darkslateblue:'#483d8b',darkslategray:'#2f4f4f',darkslategrey:'#2f4f4f',
  darkturquoise:'#00ced1',darkviolet:'#9400d3',deeppink:'#ff1493',deepskyblue:'#00bfff',
  dimgray:'#696969',dimgrey:'#696969',dodgerblue:'#1e90ff',firebrick:'#b22222',
  floralwhite:'#fffaf0',forestgreen:'#228b22',fuchsia:'#ff00ff',gainsboro:'#dcdcdc',
  ghostwhite:'#f8f8ff',gold:'#ffd700',goldenrod:'#daa520',gray:'#808080',
  grey:'#808080',green:'#008000',greenyellow:'#adff2f',honeydew:'#f0fff0',
  hotpink:'#ff69b4',indianred:'#cd5c5c',indigo:'#4b0082',ivory:'#fffff0',
  khaki:'#f0e68c',lavender:'#e6e6fa',lavenderblush:'#fff0f5',lawngreen:'#7cfc00',
  lemonchiffon:'#fffacd',lightblue:'#add8e6',lightcoral:'#f08080',lightcyan:'#e0ffff',
  lightgoldenrodyellow:'#fafad2',lightgray:'#d3d3d3',lightgrey:'#d3d3d3',
  lightgreen:'#90ee90',lightpink:'#ffb6c1',lightsalmon:'#ffa07a',lightseagreen:'#20b2aa',
  lightskyblue:'#87cefa',lightslategray:'#778899',lightslategrey:'#778899',
  lightsteelblue:'#b0c4de',lightyellow:'#ffffe0',lime:'#00ff00',limegreen:'#32cd32',
  linen:'#faf0e6',magenta:'#ff00ff',maroon:'#800000',mediumaquamarine:'#66cdaa',
  mediumblue:'#0000cd',mediumorchid:'#ba55d3',mediumpurple:'#9370db',
  mediumseagreen:'#3cb371',mediumslateblue:'#7b68ee',mediumspringgreen:'#00fa9a',
  mediumturquoise:'#48d1cc',mediumvioletred:'#c71585',midnightblue:'#191970',
  mintcream:'#f5fffa',mistyrose:'#ffe4e1',moccasin:'#ffe4b5',navajowhite:'#ffdead',
  navy:'#000080',oldlace:'#fdf5e6',olive:'#808000',olivedrab:'#6b8e23',
  orange:'#ffa500',orangered:'#ff4500',orchid:'#da70d6',palegoldenrod:'#eee8aa',
  palegreen:'#98fb98',paleturquoise:'#afeeee',palevioletred:'#db7093',
  papayawhip:'#ffefd5',peachpuff:'#ffdab9',peru:'#cd853f',pink:'#ffc0cb',
  plum:'#dda0dd',powderblue:'#b0e0e6',purple:'#800080',red:'#ff0000',
  rosybrown:'#bc8f8f',royalblue:'#4169e1',saddlebrown:'#8b4513',salmon:'#fa8072',
  sandybrown:'#f4a460',seagreen:'#2e8b57',seashell:'#fff5ee',sienna:'#a0522d',
  silver:'#c0c0c0',skyblue:'#87ceeb',slateblue:'#6a5acd',slategray:'#708090',
  slategrey:'#708090',snow:'#fffafa',springgreen:'#00ff7f',steelblue:'#4682b4',
  tan:'#d2b48c',teal:'#008080',thistle:'#d8bfd8',tomato:'#ff6347',turquoise:'#40e0d0',
  violet:'#ee82ee',wheat:'#f5deb3',white:'#ffffff',whitesmoke:'#f5f5f5',
  yellow:'#ffff00',yellowgreen:'#9acd32',
};

// ─── Color utilities ─────────────────────────────────────────────────────────

/** Parse any Cockpitdecks color value to a CSS string. */
function parseColor(value, fallback) {
  if (value == null || value === '') return fallback || '#ffffff';
  const s = String(value).trim();
  // Python tuple syntax "(r, g, b)"
  if (s.startsWith('(') && s.endsWith(')')) {
    const parts = s.slice(1, -1).split(',').map(p => parseInt(p.trim(), 10));
    return `rgb(${parts[0]},${parts[1]},${parts[2]})`;
  }
  const lower = s.toLowerCase();
  if (CSS_NAMED[lower]) return CSS_NAMED[lower];
  return s; // already hex / rgb() / etc.
}

/** Parse color to [r, g, b] array (0-255). */
function colorToRGB(value, fallback) {
  const css = parseColor(value, fallback);
  if (css.startsWith('rgb(')) {
    const m = css.match(/rgb\((\d+),(\d+),(\d+)\)/);
    if (m) return [+m[1], +m[2], +m[3]];
  }
  // hex
  let h = css.replace('#', '');
  if (h.length === 3) h = h[0]+h[0]+h[1]+h[1]+h[2]+h[2];
  if (h.length === 6) {
    return [parseInt(h.slice(0,2),16), parseInt(h.slice(2,4),16), parseInt(h.slice(4,6),16)];
  }
  return fallback ? colorToRGB(fallback) : [255, 255, 255];
}

/** Dim an RGB array by divisor (same formula as Python). */
function dimRGB(rgb, divisor) {
  const f = Math.max(divisor, 1);
  return rgb.map(c => Math.max(18, Math.floor(c / f * 2)));
}

/** Return dimmed CSS color string. */
function dimColor(value, divisor, fallback) {
  const rgb = colorToRGB(value, fallback);
  const d = dimRGB(rgb, divisor);
  return `rgb(${d[0]},${d[1]},${d[2]})`;
}

/** True if luminance < 72 (matches Python _is_dark_color). */
function isDarkColor(value) {
  const [r, g, b] = colorToRGB(value, '#000000');
  return (r * 299 + g * 587 + b * 114) / 1000 < 72;
}

// ─── YAML bool denormalisation ────────────────────────────────────────────────

/** PyYAML 1.1 turns ON/OFF into JS true/false in JSON.  Restore them. */
function yamlBoolStr(value) {
  if (value === true)  return 'ON';
  if (value === false) return 'OFF';
  return value;
}

// ─── RPN formula evaluator ────────────────────────────────────────────────────

const TOKEN_RE = /\$\{[^}]+\}|[^\s]+/g;
const PLACEHOLDER_RE = /\$\{([^}]+)\}/g;

function asNumber(v) {
  if (typeof v === 'boolean') return v ? 1 : 0;
  const n = parseFloat(v);
  return isNaN(n) ? 0 : n;
}

/** Evaluate an RPN expression, substituting ${dataref} references. */
function evalRPN(expr, datarefs, context) {
  if (expr == null) return null;
  if (typeof expr === 'number') return expr;
  const text = yamlBoolStr(expr);
  if (text == null) return null;
  const s = String(text).trim();
  if (!s) return '';

  const tokens = s.match(TOKEN_RE) || [];
  if (tokens.length === 1) return resolveToken(tokens[0], datarefs, context);

  const stack = [];
  for (const token of tokens) {
    switch (token) {
      case '+': { const b=asNumber(stack.pop()), a=asNumber(stack.pop()); stack.push(a+b); break; }
      case '-': { const b=asNumber(stack.pop()), a=asNumber(stack.pop()); stack.push(a-b); break; }
      case '*': { const b=asNumber(stack.pop()), a=asNumber(stack.pop()); stack.push(a*b); break; }
      case '/': { const b=asNumber(stack.pop()), a=asNumber(stack.pop()); stack.push(b===0?0:a/b); break; }
      case '%': { const b=asNumber(stack.pop()), a=asNumber(stack.pop()); stack.push(b===0?0:a%b); break; }
      case 'eq':  { const b=asNumber(stack.pop()), a=asNumber(stack.pop()); stack.push(a===b?1:0); break; }
      case 'min': { const b=asNumber(stack.pop()), a=asNumber(stack.pop()); stack.push(Math.min(a,b)); break; }
      case 'max': { const b=asNumber(stack.pop()), a=asNumber(stack.pop()); stack.push(Math.max(a,b)); break; }
      case 'roundn': { const d=asNumber(stack.pop()), v=asNumber(stack.pop()); stack.push(parseFloat(v.toFixed(d))); break; }
      case 'floor': stack.push(Math.floor(asNumber(stack.pop()))); break;
      case 'ceil':  stack.push(Math.ceil(asNumber(stack.pop()))); break;
      case 'round': stack.push(Math.round(asNumber(stack.pop()))); break;
      case 'abs':   stack.push(Math.abs(asNumber(stack.pop()))); break;
      default:      stack.push(resolveToken(token, datarefs, context));
    }
  }
  return stack.length ? stack[stack.length - 1] : null;
}

function resolveToken(token, datarefs, context) {
  if (token.startsWith('${') && token.endsWith('}')) {
    const key = token.slice(2, -1);
    if (context && key in context) return context[key];
    return (datarefs && key in datarefs) ? datarefs[key] : 0;
  }
  if (context && token in context) return context[token];
  const n = parseFloat(token);
  return isNaN(n) ? token : n;
}

/** Apply text-format (Python-style "{:.2f}" or "{:01.0f}") to a value. */
function applyFormat(value, fmt) {
  if (!fmt) {
    if (typeof value === 'number' && Number.isInteger(value)) return String(value);
    if (typeof value === 'number') {
      // strip trailing zeros like Python's default
      const s = String(value);
      return s.includes('.') ? s.replace(/\.?0+$/, '') : s;
    }
    return String(value ?? '');
  }
  // Handle common Python format specs: {:01.0f}, {:.2f}, {:+.1f}
  const m = fmt.match(/\{[^}]*:([^}]*)\}/);
  if (!m) return String(value ?? '');
  const spec = m[1];
  const fm = spec.match(/([+\- ]?)0?(\d*)(?:\.(\d+))?([dfegs%]?)/i);
  if (!fm) return String(value ?? '');
  const [, sign, , decimals, type] = fm;
  const n = typeof value === 'boolean' ? (value ? 1 : 0) : parseFloat(value);
  if (isNaN(n)) return String(value ?? '');
  let s;
  if (type === 'f' || type === 'e') {
    s = n.toFixed(parseInt(decimals ?? '0', 10));
  } else if (type === 'd') {
    s = String(Math.round(n));
  } else if (type === '%') {
    s = (n * 100).toFixed(parseInt(decimals ?? '0', 10)) + '%';
  } else {
    s = decimals != null ? n.toFixed(parseInt(decimals, 10)) : String(Number.isInteger(n) ? n : n);
  }
  if (sign === '+' && n >= 0) s = '+' + s;
  return s;
}

/** Substitute ${dataref} placeholders in a template string. */
function renderTemplate(template, textFormat, datarefs, context) {
  if (template == null) return '';
  const val = yamlBoolStr(template);
  if (val == null) return '';
  const raw = String(val);

  return raw.replace(PLACEHOLDER_RE, (_, key) => {
    let v = (context && key in context) ? context[key] : ((datarefs && key in datarefs) ? datarefs[key] : null);
    let fmt = textFormat;
    if (typeof textFormat === 'object' && textFormat !== null) fmt = textFormat[key] || null;
    return applyFormat(v ?? '', fmt);
  });
}

// ─── Font mapping ─────────────────────────────────────────────────────────────

const FONT_FAMILY_MAP = {
  'Segment7Standard.otf': 'Segment7Standard',
  'Seven Segment.ttf':    'Segment7Standard',
  'D-DIN-Bold.otf':       'D-DIN-Bold',
  'D-DIN.otf':            'D-DIN',
  'D-DINCondensed.otf':   'D-DINCondensed',
  'D-DINCondensed-Bold.otf': 'D-DINCondensed-Bold',
  'D-DINExp.otf':         'D-DINExp',
  'D-DINExp-Bold.otf':    'D-DINExp-Bold',
  'DIN Bold':             'D-DIN-Bold',
  'D-DIN Bold':           'D-DIN-Bold',
  'DejaVuSans.ttf':       'DejaVu Sans',
  'DejaVuSansMono.ttf':   'DejaVu Sans Mono',
  'Roboto-Regular.ttf':   'Roboto',
  'Roboto-Bold.ttf':      'Roboto',
  'B612Mono-Regular.ttf': 'B612 Mono',
  'arial.ttf':            'Arial',
  'fontawesome.otf':      'FontAwesome',
  'Font Awesome 6 Free-Regular-400.otf': 'Font Awesome 6 Free',
  'Font Awesome 6 Free-Solid-900.otf':   'Font Awesome 6 Free Solid',
};

function mapFontFamily(fontName) {
  if (!fontName) return 'system-ui, sans-serif';
  return FONT_FAMILY_MAP[fontName] || FONT_FAMILY_MAP[fontName.trim()] || fontName.replace(/\.(otf|ttf|woff2?)$/i, '');
}


function cssFont(fontName, sizePx, bold) {
  const family = mapFontFamily(fontName);
  const weight = bold ? 'bold ' : '';
  return `${weight}${Math.round(sizePx)}px "${family}", system-ui, sans-serif`;
}

/** Measure rendered text width (+ approximate height) for the given canvas context. */
function measureText(ctx, text, fontName, sizePx) {
  ctx.font = cssFont(fontName, sizePx);
  const m = ctx.measureText(text);
  const h = (m.actualBoundingBoxAscent || sizePx * 0.75) + (m.actualBoundingBoxDescent || sizePx * 0.25);
  return { width: m.width, height: h };
}

/** Find the largest font size that fits text in (maxW × maxH). */
function fitFontSize(ctx, text, fontName, maxSize, maxW, maxH, minSize) {
  minSize = minSize || 6;
  if (!text) return maxSize;
  for (let size = maxSize; size >= minSize; size--) {
    const m = measureText(ctx, text, fontName, size);
    if (m.width <= maxW && m.height <= maxH) return size;
  }
  return minSize;
}

// ─── Canvas drawing helpers ───────────────────────────────────────────────────

function roundedRect(ctx, x, y, w, h, r) {
  r = Math.min(r, w / 2, h / 2);
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

/** Draw text centered inside a rect (x0,y0)→(x1,y1). */
function drawTextInRect(ctx, x0, y0, x1, y1, text, fontName, sizePx, color, position) {
  if (!text) return;
  ctx.save();
  ctx.font = cssFont(fontName, sizePx);
  ctx.fillStyle = color;

  const w = x1 - x0;
  const h = y1 - y0;

  // position: 'ct'=center-top, 'cm'=center-middle(default), 'cb'=center-bottom
  // lt/rt/lm/rm for left/right, etc.
  const pos = (position || 'cm').toLowerCase();
  const alignH = pos.startsWith('l') ? 'left' : pos.startsWith('r') ? 'right' : 'center';
  const alignV = pos.endsWith('t') ? 'top' : pos.endsWith('b') ? 'bottom' : 'middle';

  let tx, ty;
  if (alignH === 'left')   tx = x0 + 2;
  else if (alignH === 'right') tx = x1 - 2;
  else tx = x0 + w / 2;

  if (alignV === 'top')    ty = y0 + 2;
  else if (alignV === 'bottom') ty = y1 - 2;
  else ty = y0 + h / 2;

  ctx.textAlign = alignH === 'center' ? 'center' : alignH === 'left' ? 'left' : 'right';
  ctx.textBaseline = alignV === 'middle' ? 'middle' : alignV === 'top' ? 'top' : 'bottom';
  ctx.fillText(text, tx, ty);
  ctx.restore();
}

// ─── Annunciator geometry ─────────────────────────────────────────────────────

/** Return list of {name, x0,y0,x1,y1} rects for a given annunciator model. */
function annunciatorRects(model, bx, by, bw, bh) {
  const x0 = bx + 8, y0 = by + 22, x1 = bx + bw - 8, y1 = by + bh - 8;
  if (model === 'A') return [{ name: 'A0', x0, y0, x1, y1 }];
  if (model === 'B') {
    const mid = y0 + (y1 - y0) / 2;
    return [{ name: 'B0', x0, y0, x1, y1: mid - 3 },
            { name: 'B1', x0, y0: mid + 3, x1, y1 }];
  }
  if (model === 'D') {
    const split = y0 + (y1 - y0) * 0.58;
    const mx = x0 + (x1 - x0) / 2;
    return [{ name: 'D0', x0,    y0,          x1,    y1: split - 3 },
            { name: 'D1', x0,    y0: split + 3, x1: mx - 3, y1 },
            { name: 'D2', x0: mx + 3, y0: split + 3, x1,   y1 }];
  }
  if (model === 'F') {
    const mx = x0 + (x1 - x0) / 2;
    const my = y0 + (y1 - y0) / 2;
    return [{ name: 'F0', x0,      y0,      x1: mx - 3, y1: my - 3 },
            { name: 'F1', x0: mx + 3, y0,   x1,         y1: my - 3 },
            { name: 'F2', x0,      y0: my + 3, x1: mx - 3, y1 },
            { name: 'F3', x0: mx + 3, y0: my + 3, x1,    y1 }];
  }
  return [{ name: 'A0', x0, y0, x1, y1 }];
}

/** Extract parts dict from annunciator config (supports both flat and nested). */
function annunciatorParts(annunciator) {
  if (annunciator.parts && typeof annunciator.parts === 'object') return annunciator.parts;
  const parts = {};
  for (const [k, v] of Object.entries(annunciator)) {
    if (typeof v === 'object' && v !== null && /^[A-Z]\d+$/.test(String(k))) parts[k] = v;
  }
  return parts;
}

// ─── Button rendering ─────────────────────────────────────────────────────────

function formulaContext(cfg, datarefs) {
  const ctx = {};
  if (cfg.formula != null) ctx.formula = evalRPN(cfg.formula, datarefs, {});
  return ctx;
}

function buttonTextValue(button, context, datarefs) {
  const multi = button['multi-texts'];
  if (Array.isArray(multi) && multi.length > 0) {
    const idx = Math.max(0, Math.min(multi.length - 1, Math.floor(asNumber(context.formula || 0))));
    const entry = multi[idx] || multi[0];
    return { entry, text: yamlBoolStr(entry.text || '') };
  }
  return { entry: button, text: yamlBoolStr(button.text || '') };
}

function drawAnnunciator(ctx, bx, by, bw, bh, annunciator, button, datarefs, defaults) {
  const model = String(annunciator.model || 'A');
  const rects = annunciatorRects(model, bx, by, bw, bh);
  const parts = annunciatorParts(annunciator);
  const offIntensity = annunciator['light-off-intensity'] ?? button['light-off-intensity'] ?? defaults.lightOffIntensity ?? 10;

  for (const rect of rects) {
    const part = parts[rect.name];
    if (!part) continue;
    const { x0, y0, x1, y1 } = rect;
    const rw = x1 - x0, rh = y1 - y0;

    // Panel background
    ctx.fillStyle = 'rgb(16,18,20)';
    ctx.fillRect(x0, y0, rw, rh);

    const active = !!evalRPN(part.formula != null ? part.formula : '1', datarefs, {});
    const colorVal = part.color || part['text-color'] || 'white';
    const colorRgb = colorToRGB(colorVal, '#ffffff');
    const activeColor = `rgb(${colorRgb[0]},${colorRgb[1]},${colorRgb[2]})`;
    const dimmedColor = `rgb(${dimRGB(colorRgb, offIntensity).join(',')})`;

    const ledStyle = String(part.led || '').toLowerCase();
    if (ledStyle === 'bar' || ledStyle === 'bars') {
      ctx.fillStyle = active ? activeColor : dimmedColor;
      ctx.fillRect(x0 + 8, y0 + 6, rw - 16, 8);
    } else if (ledStyle === 'dot') {
      const cx2 = (x0 + x1) / 2;
      const cy2 = (y0 + y1) / 2;
      const r = Math.max(8, Math.min(rw, rh) / 5);
      ctx.fillStyle = active ? activeColor : dimmedColor;
      ctx.beginPath();
      ctx.arc(cx2, cy2, r, 0, Math.PI * 2);
      ctx.fill();
    }

    // Part text
    const pcontext = formulaContext(part, datarefs);
    const rawText = yamlBoolStr(part.text || '');
    const renderedText = renderTemplate(rawText, part['text-format'], datarefs, pcontext);
    if (renderedText) {
      let textColor;
      if (active) {
        textColor = parseColor(part['text-color'] || colorVal);
      } else if (part['off-color']) {
        textColor = parseColor(part['off-color']);
      } else {
        textColor = dimmedColor;
      }
      const maxSize = parseInt(part['text-size'] || 28, 10);
      const fitSize = fitFontSize(ctx, renderedText, part['text-font'] || null, maxSize, rw - 12, rh - 12);
      drawTextInRect(ctx, x0, y0, x1, y1, renderedText, part['text-font'], fitSize, textColor, 'cm');
    }
  }
}

function drawButton(ctx, bx, by, bw, bh, button, defaults, datarefs, currentPageName) {
  if (!button) {
    // Empty button
    const bg = parseColor(defaults.cockpitColor, 'cornflowerblue');
    ctx.fillStyle = bg;
    ctx.fillRect(bx, by, bw, bh);
    ctx.strokeStyle = 'rgb(90,95,100)';
    ctx.lineWidth = 2;
    ctx.strokeRect(bx + 1, by + 1, bw - 2, bh - 2);
    ctx.strokeStyle = 'rgb(36,40,44)';
    ctx.lineWidth = 1;
    ctx.strokeRect(bx + 6, by + 6, bw - 12, bh - 12);
    return;
  }

  // Background
  const bgValue = button['text-bg-color'] || button['text_bg_color'];
  const bg = bgValue != null ? parseColor(bgValue) : parseColor(defaults.cockpitColor, 'cornflowerblue');
  ctx.fillStyle = bg;
  ctx.fillRect(bx, by, bw, bh);

  // Border
  ctx.strokeStyle = 'rgb(118,123,128)';
  ctx.lineWidth = 2;
  ctx.strokeRect(bx + 1, by + 1, bw - 2, bh - 2);
  ctx.strokeStyle = 'rgb(48,52,56)';
  ctx.lineWidth = 1;
  ctx.strokeRect(bx + 6, by + 6, bw - 12, bh - 12);

  const annunciator = button.annunciator;
  if (annunciator && typeof annunciator === 'object') {
    drawAnnunciator(ctx, bx, by, bw, bh, annunciator, button, datarefs, defaults);
  } else {
    // Regular text button
    const context = formulaContext(button, datarefs);
    const { entry, text: rawText } = buttonTextValue(button, context, datarefs);
    const rendered = renderTemplate(rawText, entry['text-format'] || button['text-format'], datarefs, context);
    if (rendered) {
      const textColor = parseColor(entry['text-color'] || button['text-color'] || 'white');
      const maxSize = parseInt(entry['text-size'] || button['text-size'] || defaults.textSize || 24, 10);
      const fontName = entry['text-font'] || button['text-font'] || null;
      const fitSize = fitFontSize(ctx, rendered, fontName, maxSize, bw - 16, bh - 28);
      drawTextInRect(ctx, bx + 8, by + 20, bx + bw - 8, by + bh - 8, rendered, fontName, fitSize, textColor, 'cm');
    }
  }

  // Label (small text at top of button)
  const labelRaw = button.label;
  const label = labelRaw != null ? String(yamlBoolStr(labelRaw)) : '';
  if (label) {
    const labelColor = parseColor(button['label-color'] || defaults.labelColor || 'white');
    const labelSize = parseInt(button['label-size'] || defaults.labelSize || 13, 10);
    const labelFont = button['label-font'] || defaults.labelFont || null;
    // Grey strip behind label when background is light and label is dark
    if (!isDarkColor(bg) && isDarkColor(labelColor)) {
      ctx.fillStyle = 'rgb(178,182,186)';
      ctx.fillRect(bx + 8, by + 8, bw - 16, 16);
    }
    drawTextInRect(ctx, bx + 8, by + 8, bx + bw - 8, by + 24, label, labelFont, labelSize, labelColor, 'ct');
  }

  // Active page indicator (gold outline)
  if (button.type === 'page' && button.page === currentPageName) {
    ctx.strokeStyle = 'rgb(255,188,64)';
    ctx.lineWidth = 3;
    ctx.strokeRect(bx + 2, by + 2, bw - 4, bh - 4);
  }
}

// ─── Side screen ──────────────────────────────────────────────────────────────

function drawSideScreen(ctx, sx, sy, sw, sh, button, defaults, datarefs) {
  const bg = parseColor(defaults.cockpitColor, 'cornflowerblue');
  ctx.fillStyle = bg;
  ctx.fillRect(sx, sy, sw, sh);
  ctx.strokeStyle = 'rgb(110,116,121)';
  ctx.lineWidth = 2;
  ctx.strokeRect(sx + 1, sy + 1, sw - 2, sh - 2);

  if (!button || !button.side) return;
  const labels = button.side.labels || [];
  const centers = button.side.centers || [16, 50, 84];
  for (let i = 0; i < labels.length; i++) {
    const lbl = labels[i];
    const center = centers[i] != null ? centers[i] : 16 + i * 34;
    const y = typeof center === 'number' && center <= 100 ? Math.round(sh * (center / 100)) : center;
    const context = formulaContext(lbl, datarefs);
    const title = String(lbl.label || '');
    const rendered = renderTemplate(yamlBoolStr(lbl.text || ''), lbl['text-format'], datarefs, context);
    const titleSize = parseInt(lbl['label-size'] || 14, 10);
    const valueSize = parseInt(lbl['text-size'] || 18, 10);
    const titleColor = parseColor(lbl['label-color'] || 'gold');
    const valueColor = parseColor(lbl['text-color'] || 'white');
    const titleFont = lbl['label-font'] || null;
    const valueFont = lbl['text-font'] || null;
    // Title line
    drawTextInRect(ctx, sx, sy + y - 20, sx + sw, sy + y - 2, title, titleFont, titleSize, titleColor, 'cm');
    // Value line
    drawTextInRect(ctx, sx, sy + y, sx + sw, sy + y + 22, rendered, valueFont, valueSize, valueColor, 'cm');
  }
}

// ─── Encoder column ───────────────────────────────────────────────────────────

function drawEncoderColumn(ctx, colX, colY, colW, colH, encoders) {
  const cx = colX + colW / 2;
  const encR = Math.min(colW / 2 - 6, 20);
  const positions = [colH / 6, colH / 2, colH * 5 / 6];
  for (let i = 0; i < 3; i++) {
    const enc = encoders ? encoders[i] : null;
    const ey = colY + positions[i];
    // Outer ring
    ctx.beginPath();
    ctx.arc(cx, ey, encR, 0, Math.PI * 2);
    ctx.fillStyle = '#303030';
    ctx.fill();
    ctx.strokeStyle = '#555';
    ctx.lineWidth = 1.5;
    ctx.stroke();
    // Inner ring
    ctx.beginPath();
    ctx.arc(cx, ey, encR - 5, 0, Math.PI * 2);
    ctx.fillStyle = '#222';
    ctx.fill();
    ctx.strokeStyle = '#444';
    ctx.lineWidth = 1;
    ctx.stroke();
    // Indicator dot
    ctx.beginPath();
    ctx.arc(cx, ey - encR + 4, 2.5, 0, Math.PI * 2);
    ctx.fillStyle = '#888';
    ctx.fill();
    // Name label
    if (enc) {
      const rawName = enc.name;
      const name = (rawName == null || rawName === true || rawName === false)
        ? '' : String(rawName).toUpperCase().replace(/_/g, ' ');
      if (name) {
        const fs = Math.max(7, Math.min(9, colW * 9 / (name.length * 6 + 4)));
        ctx.font = cssFont(null, fs);
        ctx.fillStyle = '#999';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        ctx.fillText(name.slice(0, 10), cx, ey + encR + 4);
      }
    }
  }
}

// ─── Pager strip ──────────────────────────────────────────────────────────────

function drawPagerStrip(ctx, stripX, stripY, stripW, stripH, pagerButtons, currentPage) {
  ctx.fillStyle = '#111';
  ctx.fillRect(stripX, stripY, stripW, stripH);

  const n = 8;
  const slotW = stripW / n;
  const r = Math.max(8, Math.min(stripH / 2 - 6, 14));
  const cy = stripY + stripH / 2;

  for (let slot = 0; slot < n; slot++) {
    const btn = pagerButtons ? pagerButtons[slot] : null;
    const cx = stripX + slot * slotW + slotW / 2;
    const target = btn ? String(btn.page || '').trim() : '';
    const colorName = btn ? String(btn['colored-led'] || '').trim() : '';
    const fullColor = colorName ? parseColor(colorName) : '#555555';
    const dimmed = dimColor(fullColor, 3);
    const isActive = target === currentPage;
    const fill = isActive ? fullColor : dimmed;

    // Circle fill
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.fillStyle = fill;
    ctx.fill();
    ctx.strokeStyle = fullColor;
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Active ring
    if (isActive) {
      ctx.beginPath();
      ctx.arc(cx, cy, r + 3, 0, Math.PI * 2);
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }

    // Slot label
    if (slot === 0) {
      const dotR = Math.max(3, Math.floor(r / 3));
      ctx.beginPath();
      ctx.arc(cx, cy, dotR, 0, Math.PI * 2);
      ctx.fillStyle = '#fff';
      ctx.fill();
    } else {
      ctx.font = cssFont(null, Math.max(8, r - 2));
      ctx.fillStyle = '#fff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(String(slot), cx, cy);
    }
  }
}

// ─── DeckRenderer class ───────────────────────────────────────────────────────

class DeckRenderer {
  /**
   * @param {HTMLCanvasElement} canvas
   * @param {object} config  — DECK_CONFIG JSON produced by yaml_to_json()
   * @param {object} [options]
   *   options.onButtonClick(key, event) — callback for button interactions
   */
  constructor(canvas, config, options) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.config = config;
    this.options = options || {};

    // Merge fixture datarefs with per-page defaults
    this.datarefs = Object.assign({}, config.datarefs || {});

    this.currentPage = null;
    this.pngImages = {}; // key → ImageData/Image (Phase 2 live mode)

    this._computeLayout();
    canvas.width  = this.hw_w;
    canvas.height = this.hw_total_h;

    canvas.addEventListener('click',      e => this._onClick(e));
    canvas.addEventListener('touchstart', e => { e.preventDefault(); this._onClick(e.touches[0]); }, { passive: false });
  }

  // ── Layout geometry ────────────────────────────────────────────────────────

  _computeLayout() {
    const L   = this.config.layout;
    const PAD = 16, GAP = 4;
    const [kw, kh] = L.keySize;
    const [cols, rows] = L.gridRepeat;
    const gap = L.gridGap ?? 8;

    const gridW = kw * cols + gap * Math.max(cols - 1, 0);
    const gridH = kh * rows + gap * Math.max(rows - 1, 0);

    let screenW = 0, screenH = 0;
    if (L.screenSize) { [screenW, screenH] = L.screenSize; }

    // LCD area (left screen + grid + right screen), no hardware encoder chrome
    const mainX  = screenW > 0 ? screenW + GAP : 0;
    const rightX = screenW > 0 ? mainX + gridW + GAP : gridW;
    const lcdW   = screenW > 0 ? rightX + screenW : gridW;
    const lcdH   = screenW > 0 ? Math.max(gridH, screenH) : gridH;

    const hasEncoders = !!L.hasEncoders;
    const pagerH = hasEncoders ? (L.pagerH ?? 42) : 0;

    const lcdX       = PAD;
    const lcdY       = PAD;
    const hw_w       = PAD + lcdW + PAD;
    const hw_body_h  = PAD + lcdH + PAD;
    const hw_total_h = hw_body_h + pagerH;

    Object.assign(this, {
      kw, kh, cols, rows, gap, gridW, gridH,
      screenW, screenH, mainX, rightX, lcdW, lcdH,
      lcdX, lcdY, hw_w, hw_body_h, hw_total_h,
      pagerH, hasEncoders, PAD, GAP,
    });
  }

  // ── Public API ─────────────────────────────────────────────────────────────

  showPage(pageName) {
    this.currentPage = pageName;
    // Sync canvas dimensions — a different deck may have resized it
    if (this.canvas.width !== this.hw_w)       this.canvas.width  = this.hw_w;
    if (this.canvas.height !== this.hw_total_h) this.canvas.height = this.hw_total_h;
    this._redraw();
  }

  updateDatarefs(delta) {
    Object.assign(this.datarefs, delta);
    this._redraw();
  }

  /** Live mode: update a single key with a pre-rendered PNG (base64 data URI or Image). */
  setPng(key, src) {
    const img = new Image();
    img.onload = () => {
      this.pngImages[key] = img;
      this._redrawLiveKey(key);
    };
    img.src = typeof src === 'string' ? src : src;
  }

  // ── Rendering ──────────────────────────────────────────────────────────────

  _redraw() {
    this._drawChrome();
    this._drawPageContent(this.currentPage);
    if (this.hasEncoders) this._drawPager();
  }

  _drawChrome() {
    const ctx = this.ctx;
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(0, 0, this.hw_w, this.hw_total_h);
  }

  _drawPageContent(pageName) {
    if (!pageName) return;
    const pageConfig = this.config.pages[pageName];
    if (!pageConfig) return;

    const { ctx, kw, kh, cols, rows, gap, lcdX, lcdY, mainX, screenW, screenH } = this;
    const defaults = this._pageDefaults(pageConfig);
    const buttons  = pageConfig.buttons || {};
    const grid = buttons.grid || {};

    // Side screens
    if (this.screenW > 0) {
      const leftBtn = buttons.left;
      const scrY = lcdY + Math.max(0, (this.lcdH - screenH) / 2);
      drawSideScreen(ctx, lcdX, scrY, screenW, screenH, leftBtn, defaults, this.datarefs);
      const rightBtn = buttons.right;
      drawSideScreen(ctx, lcdX + this.rightX, scrY, screenW, screenH, rightBtn, defaults, this.datarefs);
    }

    // Button grid
    for (let idx = 0; idx < cols * rows; idx++) {
      const row = Math.floor(idx / cols);
      const col = idx % cols;
      const bx = lcdX + mainX + col * (kw + gap);
      const by = lcdY + row * (kh + gap);
      const button = grid[String(idx)] || grid[idx] || null;
      drawButton(ctx, bx, by, kw, kh, button, defaults, this.datarefs, pageName);
    }

  }

  _drawPager() {
    const pagerConfig = this.config.pager || {};
    drawPagerStrip(this.ctx, 0, this.hw_body_h, this.hw_w, this.pagerH, pagerConfig, this.currentPage);
  }

  _pageDefaults(pageConfig) {
    const global = this.config.defaults || {};
    return {
      cockpitColor:    parseColor(pageConfig['cockpit-color'] || global['cockpit-color'] || 'cornflowerblue'),
      textSize:        pageConfig['default-text-size']  || global['default-text-size']  || 24,
      labelSize:       pageConfig['default-label-size'] || global['default-label-size'] || 13,
      labelColor:      pageConfig['default-label-color'] || global['default-label-color'] || 'white',
      labelFont:       pageConfig['default-label-font']  || global['default-label-font']  || null,
      lightOffIntensity: pageConfig['default-light-off-intensity'] || global['default-light-off-intensity'] || 10,
    };
  }

  // ── Live mode (Phase 2): redraw a single key from a pre-received PNG ────────

  _redrawLiveKey(key) {
    const img = this.pngImages[key];
    if (!img) return;
    const { kw, kh, cols, lcdX, lcdY, mainX, gap } = this;
    const idx = typeof key === 'string' ? parseInt(key, 10) : key;
    if (!isNaN(idx)) {
      const row = Math.floor(idx / cols);
      const col = idx % cols;
      const bx = lcdX + mainX + col * (kw + gap);
      const by = lcdY + row * (kh + gap);
      this.ctx.drawImage(img, bx, by, kw, kh);
    }
  }

  // ── Click / touch handling ─────────────────────────────────────────────────

  _onClick(e) {
    const rect = this.canvas.getBoundingClientRect();
    const sx = this.canvas.width  / rect.width;
    const sy = this.canvas.height / rect.height;
    const x = (e.clientX - rect.left) * sx;
    const y = (e.clientY - rect.top)  * sy;

    // Check pager strip
    if (this.hasEncoders && y >= this.hw_body_h) {
      const pager = this.config.pager || {};
      const n = 8;
      const slotW = this.hw_w / n;
      const slot = Math.floor(x / slotW);
      const btn = pager[slot];
      if (btn && btn.page) { this.showPage(btn.page); return; }
    }

    if (!this.currentPage) return;
    const pageConfig = this.config.pages[this.currentPage];
    if (!pageConfig) return;

    const grid = (pageConfig.buttons || {}).grid || {};
    const { kw, kh, cols, rows, lcdX, lcdY, mainX, gap } = this;

    for (let idx = 0; idx < cols * rows; idx++) {
      const row = Math.floor(idx / cols);
      const col = idx % cols;
      const bx = lcdX + mainX + col * (kw + gap);
      const by = lcdY + row * (kh + gap);
      if (x >= bx && x <= bx + kw && y >= by && y <= by + kh) {
        const button = grid[String(idx)] || grid[idx];
        if (button) {
          if (button.type === 'page' && button.page) {
            this.showPage(button.page);
          } else if (this.options.onButtonClick) {
            this.options.onButtonClick(idx, button);
          }
        }
        return;
      }
    }
  }
}
