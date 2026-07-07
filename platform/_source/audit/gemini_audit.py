#!/usr/bin/env python3
"""Independent visual+UX audit of the HyperPlatform Минцифры accreditation page via Gemini (AI Studio key)."""
import sys, os
from pathlib import Path
from google import genai
from google.genai import types

HERE = Path(__file__).parent

PROMPT = """[РАУНД 3 — ФИНАЛЬНОЕ ПОДТВЕРЖДЕНИЕ] Доп. правки после раунда 2: на мобайле усилено разделение между КАТЕГОРИЯМИ функционала (каждая категория = отдельная bordered-карточка с увеличенным отступом); контраст ссылок в футере поднят. Скриншоты раунда 3 (desktop full, desktop детально функционал, MOBILE функционал крупно, руководство). Дай финальную оценку по тем же 7 измерениям и итог; подтверди, готова ли страница к сдаче.

Ты — старший арт-директор и одновременно ревьюер сайтов на соответствие требованиям Минцифры РФ к ИТ-сайтам. Перед тобой скриншоты ОТДЕЛЬНОЙ страницы аккредитации для ПО «Хайперплатформ» (HyperPlatform — платформа для чат-ботов; правообладатель ООО «Хайперпартнер»).

Контекст и намерение:
- Это НЕ маркетинговый лендинг, а официальная информационная страница под проверку аккредитации ИТ-компании в Минцифры. Цель — выглядеть достоверно, профессионально, читаемо; покрыть чек-лист (правообладатель, назначение, стоимость, функц. характеристики, документация, поддержка).
- Дизайн намеренно сдержанный, «документ-стайл», в брендинге HyperPartner: IBM Plex Sans, тёмно-зелёный forest #16302B (хедер/футер/блок стоимости), бронза #C79A7E (акцент), светлый фон paper #F5F4F0, мятные галочки.
- Скриншоты: 1) десктоп full-page; 2) блок «Стоимость»+«Документация» десктоп; 3) футер+поддержка десктоп; 4) мобайл full-page (393px); 5) руководство пользователя (под-страница) верх; 6) руководство — раздел с таблицами.

Проведи ЖЁСТКИЙ аудит. Не хвали ради вежливости — ищи реальные проблемы. Для КАЖДОГО измерения дай оценку 1–10 и обоснование:
1. Визуальная иерархия и композиция
2. Типографика (размеры, межстрочный, ритм, переносы, «сироты»)
3. Спейсинг и вертикальный ритм
4. Цвет, контраст (читаемость, доступность), бренд-консистентность
5. Мобильная адаптация (393px)
6. Профессионализм/достоверность для гос-проверки
7. Читаемость и удобство (карточки, списки, таблицы руководства)

Затем дай список КОНКРЕТНЫХ проблем, каждая в формате:
[severity: BLOCKER|MAJOR|MINOR] <что не так и где> → <конкретная правка>

В конце — ИТОГОВАЯ оценка (1–10) и вердикт: готово к сдаче / нужны правки. Отвечай по-русски, структурировано, без воды."""

parts = [types.Part.from_text(text=PROMPT)]
imgs = ["r3-desk-full.jpeg", "r2-features2.jpeg", "r3-mob-features.jpeg", "g-desk-top.jpeg"]
used = []
for img in imgs:
    p = HERE / img
    if p.exists():
        parts.append(types.Part.from_bytes(data=p.read_bytes(), mime_type="image/jpeg"))
        used.append(img)
sys.stderr.write(f"images: {used}\n")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
for model in ("gemini-2.5-pro", "gemini-2.5-flash"):
    try:
        resp = client.models.generate_content(
            model=model,
            contents=[types.Content(role="user", parts=parts)],
            config=types.GenerateContentConfig(
                temperature=0.6,
                thinking_config=types.ThinkingConfig(thinking_budget=8000),
            ),
        )
        out = resp.text or "(empty)"
        (HERE / "gemini_audit_r3.md").write_text(f"# Gemini audit ({model})\n\n{out}", encoding="utf-8")
        sys.stderr.write(f"OK {model}: {len(out)} chars -> gemini_audit_r1.md\n")
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"[{model} failed: {e}]\n")
sys.exit(1)
