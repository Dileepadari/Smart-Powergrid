<?php
include("classes/database.php");
if ($_SERVER["REQUEST_METHOD"] == "POST") {
echo "the data is coming";
$json = file_get_contents('php://input');
$data = json_decode($json, true);
print_r($data);
		$sensor = $data["sensor"];
        $temperature = $data["Temperature"];
		$humidity = $data["Humidity"];
print_r($sensor);
echo $temperature;
echo $humidity;

		$query = "insert into DHT_Readings 
		(Temperature, Humidity, avg_Temperature, avg_humidity) 
		values 
		('$temperature','$humidity','$sensor', '234')";
        echo $query;

		$DB = new Database();
		$DB->save($query);
}
		
?>