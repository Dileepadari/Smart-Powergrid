<?php
include("classes/database_c.php");
if ($_SERVER["REQUEST_METHOD"] == "POST") {
$json = file_get_contents('php://input');
$data = json_decode($json, true);
		$user_name = $data["user"];
        $key = $data["key"];
		$message = $data["msg"];
        $appliance = $data["appliance"];
if($key == "1234"){
            $query = "select * from Users where username = '$user_name' limit 1 ";
			$DB = new Database();
			$result = $DB->read($query);
			if($result)
			{
					$userid = $result[0]['userid'];
					
					$query = "insert into Notifications (notification_msg, appliance, userid, seen) values 
	            	('$message','$appliance','$userid', 0)";
            		$DB = new Database();
	            	$DB->save($query);
	            	echo "successufully sent !";
		   	}
			
}
else{
// 		$query = "insert into DHT_Readings 
// 		(Temperature, Humidity, avg_Temperature, avg_humidity) 
// 		values 
// 		('$temperature','$humidity','$sensor', '234')";
//         echo $query;

// 		$DB = new Database();
// 		$DB->save($query);
echo "key is wrong !";
}
}
else{
echo "You are not authorised !";
}

?>