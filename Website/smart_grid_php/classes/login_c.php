<?php
session_start();
include("database_c.php");

class Login
{

	private $error = "";
 
	public function evaluate($data)
	{
		$user_type = $data['user_type'];
		$email = addslashes($data['email']);
		$password = addslashes($data['password']);
		$query = "select * from Users where email = '$email' AND user_type='$user_type' limit 1 ";
		
		$DB = new Database();
		$result = $DB->read($query);
		
		if($result)
		{
			
			$row = $result[0];
			
			// if($this->hash_text($password) == $row['password'])
			if($password == $row['password'])
			{
				
				//create session data
				$_SESSION['IOT_userid'] = $row['userid'];
				
			}else
			{
				$this->error .= "wrong email or password<br>";
			}
		}else
		{

			$this->error .= "wrong email or password<br>";
		}

		return $this->error;
		
	}

	private function hash_text($text){

		$text = hash("sha1", $text);
		return $text;
	}

	public function check_login($userid,$redirect = 1)
	{
		if(is_numeric($userid))
		{			
			$query = "select * from Users where userid = '$userid' limit 1 ";
			$DB = new Database();
			$result = $DB->read($query);
			if($result)
			{	
				$user_data = $result[0];
				return $user_data;
			
			}else
			{ 
				if($redirect){
					header("Location: login.php");
					die;
				}else{

					$_SESSION['IOT_userid'] = 0;
				}
			}
 
			 
		}else
		{
			if($redirect){
				header("Location: login.php");
				die;
			}else{
				$_SESSION['IOT_userid'] = 0;
			}
		}

	}
	public function check_admin_login($userid,$redirect = 1)
	{
		if(is_numeric($userid))
		{

			$query = "select * from Users where userid = '$userid' AND user_type = 'admin' limit 1 ";
			$DB = new Database();
			$result = $DB->read($query);
			if($result)
			{
					$user_data = $result[0];
					return $user_data;
			}
			else
			{ 
				if($redirect){
					return 0;
					die;
				}else{

					$_SESSION['IOT_userid'] = 0;
				}
			}
 
			 
		}else
		{
			if($redirect){
				return 0;
				die;
			}else{
				$_SESSION['IOT_userid'] = 0;
			}
		}

	}
}
?>