"""UT용 단축어(chi2kawa-ut)를 코드로 만든다.

단축어 하나로 두 가지 일을 한다(참가자가 여러 개 설치하지 않게).
  입력이 없으면(알림 Task, 페이지가 입력 없이 실행):
      2분 뒤 시각으로 미리 알림("방금 커피 한 잔이 증발했어요")을 등록하고 인스타그램을 연다.
  입력이 있으면(불러오기, 페이지가 참가자 코드를 입력으로 넘김):
      1) 앱 및 웹사이트 활동 가져오기(기간: 오늘)
      2) <페이지 주소>?pid=<단축어 입력>#d=<값> 을 사파리로 연다.
페이지는 shortcuts://run-shortcut?name=<단축어 이름>&input=text&text=<pid> 로 실행해 참가자 코드를 넘긴다.
단축어가 기본 브라우저로 페이지를 다시 열기 때문에, 처음 연 브라우저와 달라도 참가자 코드가 이어지게 하려는 것이다.

  --no-data 없이: #d= 뒤에 앱별 사용 시간 목록을 싣는다(iOS가 보내기·출력 허용을 묻는다). UT는 이 방식을 쓴다.
  --no-data:      #d=1 만 붙인다. 사용 시간은 가져오기만 하고 페이지로 넘기지 않는다.
UT 페이지는 #d= 목록에서 인스타그램 시간만 읽는다.

사용법 (macOS):
  python3 make_shortcut.py https://chi2kawa-ut.vercel.app/ [--no-data] > build/TimeMoneyUT-unsigned.shortcut
  shortcuts sign --mode anyone --input build/TimeMoneyUT-unsigned.shortcut --output ../public/chi2kawa-ut.shortcut
받은 파일 이름이 곧 단축어 이름이 된다(chi2kawa-ut). 한글 이름은 기기마다 저장 방식(NFC/NFD)이 달라
웹의 run-shortcut이 못 찾는 일이 있어 영문으로 둔다.
"""
import plistlib
import sys
import uuid

USAGE_ACTION = (
    "com.apple.intelligenceplatform.IntelligencePlatform."
    "IntelligencePlatformDataActionsAppIntentsExtension.CalculateAppUsageIntent"
)
OBJ = "￼"
SHORTCUT_INPUT = {"Type": "ExtensionInput"}
ALERT_TITLE = "방금 커피 한 잔이 증발했어요"
ALERT_NOTE = "인스타그램을 보는 사이 커피 한 잔 값이 증발했어요. 브라우저로 돌아가 확인해 보세요."


def output_of(action_uuid, name):
    return {"OutputUUID": action_uuid, "Type": "ActionOutput", "OutputName": name}


def token_string(parts):
    """문자열과 변수를 섞어 WFTextTokenString을 만든다. parts: str 또는 변수 dict의 목록."""
    text, attachments = "", {}
    for part in parts:
        if isinstance(part, str):
            text += part
        else:
            attachments["{%d, 1}" % len(text)] = part
            text += OBJ
    return {"Value": {"string": text, "attachmentsByRange": attachments}, "WFSerializationType": "WFTextTokenString"}


# 마지막 동작이 남긴 값(연 주소 텍스트)은 단축어의 실행 결과로 호출한 사파리에 돌아가려 해서
# iOS가 "텍스트 항목을 출력하도록 허용" 창을 띄운다. 분기 끝에서 결과를 비워 그 창이 뜨지 않게 한다.
NOTHING = {"WFWorkflowActionIdentifier": "is.workflow.actions.nothing", "WFWorkflowActionParameters": {}}


def alert_actions():
    """미리 알림을 먼저 만들고 인스타그램을 연다. 처음 실행할 때 뜨는 미리 알림 접근 허용 창이
    인스타그램 뒤에 숨지 않게 하려는 것이다. 인스타그램이 없으면 페이지가 곧바로 돌아온 것을 보고 피드로 잇는다."""
    date_id = str(uuid.uuid4()).upper()
    return [
        {"WFWorkflowActionIdentifier": "is.workflow.actions.adjustdate",
         "WFWorkflowActionParameters": {
             "UUID": date_id,
             "WFDate": token_string([{"Type": "CurrentDate"}]),
             "WFAdjustOperation": "Add",
             "WFDuration": {"Value": {"Unit": "min", "Magnitude": "2"}, "WFSerializationType": "WFQuantityFieldValue"}}},
        {"WFWorkflowActionIdentifier": "is.workflow.actions.addnewreminder",
         "WFWorkflowActionParameters": {
             "WFCalendarItemTitle": ALERT_TITLE,
             "WFCalendarItemNotes": ALERT_NOTE,
             "WFAlertEnabled": "Alert",
             "WFAlertCustomTime": token_string([output_of(date_id, "조정된 날짜")])}},
        {"WFWorkflowActionIdentifier": "is.workflow.actions.openurl",
         "WFWorkflowActionParameters": {"WFInput": token_string(["instagram://app"])}},
        NOTHING,
    ]


def build(page, include_data=True, during="today"):
    usage_id = str(uuid.uuid4()).upper()
    base = page.split("#")[0].split("?")[0]
    actions = [
        {"WFWorkflowActionIdentifier": USAGE_ACTION,
         "WFWorkflowActionParameters": {"UUID": usage_id, "during": during}},
    ]
    if include_data:
        text_id, enc_id = str(uuid.uuid4()).upper(), str(uuid.uuid4()).upper()
        actions += [
            {"WFWorkflowActionIdentifier": "is.workflow.actions.text.combine",
             "WFWorkflowActionParameters": {
                 "UUID": text_id,
                 # 구분자를 비우면 기기에 따라 한 줄로 합쳐져 앱별 시간을 나눠 읽을 수 없다
                 "WFTextSeparator": "New Lines",
                 "text": {"Value": output_of(usage_id, "활동"), "WFSerializationType": "WFTextTokenAttachment"}}},
            {"WFWorkflowActionIdentifier": "is.workflow.actions.urlencode",
             "WFWorkflowActionParameters": {
                 "UUID": enc_id, "WFEncodeMode": "Encode",
                 "WFInput": token_string([output_of(text_id, "합쳐진 텍스트")])}},
        ]
        tail = ["#d=", output_of(enc_id, "URL 인코딩된 텍스트")]
    else:
        tail = ["#d=1"]
    actions.append({
        "WFWorkflowActionIdentifier": "is.workflow.actions.openurl",
        "WFWorkflowActionParameters": {"WFInput": token_string([base + "?pid=", SHORTCUT_INPUT] + tail)}})
    actions.append(NOTHING)
    group = str(uuid.uuid4()).upper()
    branch = lambda mode, extra=None: {
        "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
        "WFWorkflowActionParameters": {"GroupingIdentifier": group, "WFControlFlowMode": mode, **(extra or {})}}
    actions = (
        # 글자 비교 조건은 단축어 앱에서 비교 값이 비어 버려서, 비교 값이 필요 없는 '값이 있음'(100) 조건으로 나눈다
        [branch(0, {"WFCondition": 100,
                    "WFInput": {"Type": "Variable", "Variable": {"Value": SHORTCUT_INPUT, "WFSerializationType": "WFTextTokenAttachment"}}})]
        + actions + [branch(1)] + alert_actions() + [branch(2, {"UUID": str(uuid.uuid4()).upper()})]
    )
    return {
        "WFWorkflowActions": actions,
        "WFWorkflowClientVersion": "4711",
        "WFWorkflowMinimumClientVersion": 900,
        "WFWorkflowMinimumClientVersionString": "900",
        "WFWorkflowIcon": {"WFWorkflowIconStartColor": 4274264319, "WFWorkflowIconGlyphNumber": 59511},
        "WFWorkflowTypes": [],
        "WFWorkflowInputContentItemClasses": ["WFStringContentItem"],
        "WFWorkflowOutputContentItemClasses": [],
        "WFWorkflowImportQuestions": [],
        "WFWorkflowHasShortcutInputVariables": True,
        "WFWorkflowHasOutputFallback": False,
        "WFQuickActionSurfaces": [],
    }


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit("페이지 주소가 필요합니다. 예: python3 make_shortcut.py https://chi2kawa-ut.vercel.app/")
    plistlib.dump(build(args[0], include_data="--no-data" not in sys.argv), sys.stdout.buffer, fmt=plistlib.FMT_BINARY)
