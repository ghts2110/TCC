import re
from typing import List, Dict, Optional

RG_RE   = re.compile(r"\b(\d{1,2}\.?\d{3}\.?\d{3}|\d{7,9})\b")
CPF_RE  = re.compile(r"\b(\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{11})\b")
DATE_RE = re.compile(r"\b([0-3]\d)[/\-]([0-1]\d)[/\-]((?:19|20)\d{2})\b")
BRACK_RE = re.compile(r"<<\s*(.+?)\s*>>")

LABELS = {
    "rg": re.compile(r"(registro\s*geral|\brg\b)", re.I),
    "nome": re.compile(r"^\s*nome\b", re.I),
    "data_nascimento": re.compile(r"data\s*de\s*nascimento", re.I),
    "data_expedicao_full": re.compile(r"data\s*de\s*expedi", re.I),  
    "data_de_only": re.compile(r"^\s*data\s*de\s*$", re.I),         
    "expedicao_line": re.compile(r"^\s*expedi", re.I),               
    "naturalidade": re.compile(r"^\s*naturalidade\b", re.I),
    "filiacao": re.compile(r"^\s*filia[cç][aã]o\b", re.I),
    "doc_origem": re.compile(r"doc\.\s*origem", re.I),
    "orgao_emissor": re.compile(r"org[aã]o\s*emissor|ssp(?:\/[a-z]{2})?", re.I),
    "cpf": re.compile(r"\bcpf\b", re.I),
}

def _norm_lines(raw_text: str) -> List[str]:
    lines = [re.sub(r"\s{2,}", " ", l.strip()) for l in raw_text.splitlines()]
    return [l for l in lines if l]

def _next_idx(i: int, lines: List[str]) -> Optional[int]:
    j = i + 1
    while j < len(lines) and not lines[j].strip():
        j += 1
    return j if j < len(lines) else None

def _clean_brackets(s: str) -> str:
    m = BRACK_RE.search(s)
    return (m.group(1) if m else s).strip(" <>")

def _is_any_label(line: str) -> bool:
    return any(p.search(line) for p in LABELS.values())

def _format_cpf(cpf_digits: str) -> str:
    d = re.sub(r"\D", "", cpf_digits)
    if len(d) == 11:
        return f"{d[0:3]}.{d[3:6]}.{d[6:9]}-{d[9:11]}"
    return cpf_digits

def _cpf_valido(cpf: str) -> bool:
    # Validação padrão de CPF (ignora máscaras)
    s = re.sub(r"\D", "", cpf)
    if len(s) != 11 or s == s[0] * 11:
        return False
    # 1º dígito
    soma = sum(int(s[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10) % 11
    if d1 == 10: d1 = 0
    if d1 != int(s[9]): return False
    # 2º dígito
    soma = sum(int(s[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10) % 11
    if d2 == 10: d2 = 0
    return d2 == int(s[10])

def extract_fields(raw_text: str) -> Dict[str, object]:
    lines = _norm_lines(raw_text)

    out = {
        "nome": None,
        "rg": None,
        "cpf": None,
        "cpf_valido": None,       
        "data_nascimento": None,
        "data_expedicao": None,
        "naturalidade": None,
        "filiacao": [],
        "orgao_emissor": None,
        "doc_origem": None,
    }

    # 1) Captura CPF espalhado, formata e valida
    for l in lines:
        if out["cpf"]:
            break
        mcpf = CPF_RE.search(l)
        if mcpf:
            out["cpf"] = _format_cpf(mcpf.group(1))
            out["cpf_valido"] = _cpf_valido(out["cpf"])

    i = 0
    while i < len(lines):
        line = lines[i]

        # --- RG ---
        if LABELS["rg"].search(line):
            m = RG_RE.search(line)
            if m:
                out["rg"] = m.group(1)
            else:
                j = _next_idx(i, lines)
                if j is not None:
                    m = RG_RE.search(lines[j])
                    if m:
                        out["rg"] = m.group(1)
                        i = j  # avança, pois consumimos a próxima linha
        # se ainda não achou RG, tente padrão solto "X.XXX.XXX" logo abaixo do bloco do cabeçalho
        if not out["rg"]:
            mrg_loose = RG_RE.search(line)
            if mrg_loose and not _is_any_label(line):
                out["rg"] = mrg_loose.group(1)

        # --- NOME ---
        if LABELS["nome"].search(line):
            # examina as próximas 6 linhas
            window = [line] + [lines[i+k] for k in range(1,7) if i+k < len(lines)]
            name = None
            for cand in window:
                # ignora linhas tipo "VÁLIDA ..."
                if "VÁLIDA" in cand.upper():
                    continue
                m = BRACK_RE.search(cand)
                if m:
                    name = m.group(1).strip()
                    break
            if not name:
                for cand in window:
                    if not _is_any_label(cand) and cand.isupper() and len(cand) > 5:
                        name = cand.strip()
                        break
            if name:
                out["nome"] = _clean_brackets(name)

        # --- DATA DE EXPEDIÇÃO ---
        # casos:
        #  a) "DATA DE EXPEDIÇÃO 01/07/2015" (mesma linha)
        #  b) "DATA DE" | na próxima linha "EXPEDIÇÃO 01/07/2015"
        #  c) "DATA DE EXPEDIÇÃO" | próxima linha só a data
        if LABELS["data_expedicao_full"].search(line):
            m = DATE_RE.search(line)
            if m:
                out["data_expedicao"] = m.group(0)
            else:
                j = _next_idx(i, lines)
                if j is not None:
                    # pode estar na linha seguinte
                    m = DATE_RE.search(lines[j])
                    if m:
                        out["data_expedicao"] = m.group(0)
                        i = j
        elif LABELS["data_de_only"].search(line):
            # Próxima linha deve começar com "EXPEDI..." e conter a data
            j = _next_idx(i, lines)
            if j is not None and LABELS["expedicao_line"].search(lines[j]):
                m = DATE_RE.search(lines[j])
                if m:
                    out["data_expedicao"] = m.group(0)
                    i = j

        # --- DATA DE NASCIMENTO ---
        if LABELS["data_nascimento"].search(line):
            m = DATE_RE.search(line)
            if m:
                out["data_nascimento"] = m.group(0)
            else:
                j = _next_idx(i, lines)
                if j is not None:
                    m = DATE_RE.search(lines[j])
                    if m:
                        out["data_nascimento"] = m.group(0)
                        i = j

        # --- NATURALIDADE ---
        if LABELS["naturalidade"].search(line):
            j = _next_idx(i, lines)
            if j is not None:
                out["naturalidade"] = _clean_brackets(lines[j])
                i = j

        # --- FILIAÇÃO (até duas linhas) ---
        if LABELS["filiacao"].search(line):
            j = _next_idx(i, lines)
            if j is not None:
                out["filiacao"].append(_clean_brackets(lines[j]))
                k = _next_idx(j, lines)
                if k is not None and not _is_any_label(lines[k]):
                    out["filiacao"].append(_clean_brackets(lines[k]))
                    i = k

        # --- DOC. ORIGEM / Órgão emissor (quando presente) ---
        if LABELS["doc_origem"].search(line):
            m = BRACK_RE.search(line)
            if m:
                out["doc_origem"] = m.group(1).strip()
            else:
                j = _next_idx(i, lines)
                if j is not None:
                    out["doc_origem"] = _clean_brackets(lines[j])

        if LABELS["orgao_emissor"].search(line) or ("SSP" in line):
            m = re.search(r"(SSP[\s/.-]?[A-Z]{2})", line)
            if not m:
                j = _next_idx(i, lines)
                if j is not None:
                    m = re.search(r"(SSP[\s/.-]?[A-Z]{2})", lines[j])
                    if m:
                        out["orgao_emissor"] = m.group(1)
                        i = j
            else:
                out["orgao_emissor"] = m.group(1)
                
        i += 1

    # Normalizações finais
    if out["rg"]:
        out["rg"] = out["rg"].replace(" ", "")
    if out["cpf"] and out["cpf_valido"] is None:
        out["cpf_valido"] = _cpf_valido(out["cpf"])

    return out
