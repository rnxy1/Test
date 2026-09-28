import re
_DIAC = re.compile('[ؐ-ًؚ-ٰٟۖ-ۭـ]')
_DIG = str.maketrans('٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹', '01234567890123456789')
def norm(s):
    s = _DIAC.sub('', s or '').translate(_DIG)
    s = re.sub('[أإآٱ]', 'ا', s).replace('ة', 'ه').replace('ى', 'ي').replace('ؤ', 'و').replace('ئ', 'ي')
    return re.sub(r'\s+', ' ', s).strip().lower()
