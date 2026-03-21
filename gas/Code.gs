/**
 * 自動化帝国 プレイログ収集 GAS
 * スプレッドシートにプレイデータを自動追記する
 */

function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = JSON.parse(e.postData.contents);

  // ヘッダー行がなければ追加
  if (sheet.getLastRow() === 0) {
    sheet.appendRow([
      "日時",
      "セッションID",
      "プレイ時間(秒)",
      "総ターン数",
      "最長シーン",
      "最長シーン%",
      "最多案件",
      "最多案件回数",
      "サボり回数",
      "デフラグ回数",
      "案件種類数",
      "詰まりポイント数",
      "ブラウザ"
    ]);
  }

  sheet.appendRow([
    new Date().toISOString(),
    data.session_id || "",
    Math.round(data.total_play_secs || 0),
    data.total_turns || 0,
    data.top_scene || "",
    data.top_scene_pct || 0,
    data.top_job || "",
    data.top_job_count || 0,
    data.idle_count || 0,
    data.defrag_count || 0,
    data.job_variety || 0,
    data.stuck_points || 0,
    data.user_agent || ""
  ]);

  return ContentService.createTextOutput(
    JSON.stringify({ status: "ok" })
  ).setMimeType(ContentService.MimeType.JSON);
}

// GETアクセス時のテスト用
function doGet(e) {
  return ContentService.createTextOutput(
    JSON.stringify({ status: "ok", message: "Play log endpoint is running" })
  ).setMimeType(ContentService.MimeType.JSON);
}
