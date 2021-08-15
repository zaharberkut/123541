<?php
$access_token = "4ab815466027d38b-e97c7093d9e82f2a-340eb796a8ff9f0";
$request = file_get_contents("php://input");
$input = json_decode($request, true);
$json_weather = file_get_contents("https://api.weatherlink.com/v1/NoaaExt.json?user=001D0A0124D3&pass=zaharberkut2019&
apiToken=ED47A9235AF1472A8B5BC594D830B39D");
$data_weather = json_decode($json_weather, true);
$pressure = round($data_weather['pressure_mb'] * 0.75006375541921,1);
$temperature = $data_weather['temp_c'];
$wind_speed = round($data_weather['wind_mph'] * 0.44704,1);
$wind_direction = $data_weather['wind_dir'];
$humidity = $data_weather['relative_humidity'];
$rain_ratehr = round($data_weather['davis_current_observation']['rain_rate_in_per_hr'] * 25.4,2);
$rain_dayin = round($data_weather['davis_current_observation']['rain_day_in'] * 25.4,2);

switch ($wind_direction) {
    case "North":
        $wind_dir_uk = "Північний";
        break;
    case "South":
        $wind_dir_uk = "Південний";
        break;
    case "West":
        $wind_dir_uk = "Західний";
        break;
    case "East":
        $wind_dir_uk = "Східний";
        break;
    case "North-northeast":
        case "Northeast":
            case "East-northeast":
                $wind_dir_uk = "Північно-Східний";
                break;
    case "North-northwest":
        case "West-northwest":
            case "Northwest":
                $wind_dir_uk = "Північно-Західний";
                break;
    case "South-southeast":
        case "East-southeast":
            case "Southeast":
            $wind_dir_uk = "Південно-Східний";
            break;
    case "South-southwest":
        case "Southwest":
            case "West-southwest":
                $wind_dir_uk = "Південно-Західний";
                break;
}
$collecting_data = "Температура: $temperature C\n". "Тиск: $pressure мм рт. ст.\n". "Вологість: $humidity%\n".
	"Швидкість вітру: $wind_speed м/с\n". "Напрямок вітру: $wind_dir_uk\n". "Опади: $rain_dayin мм/день, $rain_ratehr мм/год.";
date_default_timezone_set('Europe/Kiev');
$date1 = date('G:i');
if($input['event']=='webhook') {
    $webhook_response['status'] = 0;
    $webhook_response['status_message'] = "ok";
    $webhook_response['event_tyes'] = "delivered";
    echo json_encode($webhook_response);
    die;
}
else if($input['event']=='message') {
    $text_received = $input['message']['text'];
    $sender_id = $input['sender']['id'];
    $sender_name = $input['sender']['name'];
    $data['keyboard'] = keyboardTemplate()['keyboard'];

	if ($text_received=="weather"){
		$message_to_reply = "Вітаю "."$sender_name. \n"."Погода станом на "."$date1 \n"."======================\n"."$collecting_data";
	}
	 else if($text_received=='menu'){
		$message_to_reply = "select";
		$data['keyboard'] = keyboardTemplate()['keyboard'];
	 }
	else{
		$message_to_reply = "Вітаю "."$sender_name. \n"."Погода станом на "."$date1 \n"."======================\n"."$collecting_data";
	}
    $data['auth_token'] = $access_token;
    $data['receiver'] = $sender_id;
    $data['type'] = "text";
    $data['text'] = $message_to_reply;
    sendMessage($data);
}
function keyboardTemplate(){
	$keyboard_array['Type'] = 'keyboard';
	$keyboard_array['DefaultHeight'] = false;
	$keyboard_array['BgColor'] = '#f7bb3f';
	$keyboard['keyboard'] = $keyboard_array;


		$keyboard_properties['Columns'] = 6;
		$keyboard_properties['Rows'] = 1;
#		$keyboard_properties['TextValign'] = "top";
#		$keyboard_properties['TextHalign'] = "top";
		$keyboard_properties['TextOpacity'] = "100";
		$keyboard_properties['Text'] = '<font color=\"#494E67\"><b>Отримати погоду</b></font>';
		$keyboard_properties['TextSize'] = "large";
		$keyboard_properties['ActionType'] = "reply";
		$keyboard_properties['ActionBody'] = "weather";
		$keyboard_properties['BgColor'] = "#f7bb3f";
#		$keyboard_properties['Image'] = "https://zaharberkutweather.herokuapp.com/21.png";
		$keyboard['keyboard']['Buttons'][] = $keyboard_properties;

	return $keyboard;
}
function sendMessage($data) {
    $url = "https://chatapi.viber.com/pa/send_message";
    $jsonData = json_encode($data);
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type/json'));
    $result = curl_exec($ch);
    return $result;
}
?>
