<?php
class Database
{

	private $host = "localhost";
	private $username = "id20700254_delhi";
	private $password = "Delhiking@143";
	private $db = "id20700254_smart_database";

	function connect()
	{

		$connection = mysqli_connect($this->host,$this->username,$this->password,$this->db);
		return $connection;
	}

	function read($query)
	{
		$conn = $this->connect();
		$result = mysqli_query($conn,$query);

		if(!$result)
		{
			return false;
		}
		else
		{
			$data = false;
			while($row = mysqli_fetch_assoc($result))
			{

				$data[] = $row;

			}

			return $data;
		}
	}

	function save($query)
	{
		$conn = $this->connect();
		$result = mysqli_query($conn,$query);

		if(!$result)
		{
			return false;
		}else
		{
		    return true;
		}
	}

}

?>