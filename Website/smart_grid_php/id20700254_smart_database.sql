-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 20, 2023 at 12:43 PM
-- Server version: 10.5.20-MariaDB
-- PHP Version: 7.3.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `id20700254_smart_database`
--

-- --------------------------------------------------------

--
-- Table structure for table `Notifications`
--

CREATE TABLE `Notifications` (
  `id` int(10) NOT NULL,
  `userid` int(50) NOT NULL,
  `notification_msg` varchar(300) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  `appliance` varchar(100) NOT NULL,
  `seen` int(2) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `Notifications`
--

INSERT INTO `Notifications` (`id`, `userid`, `notification_msg`, `date`, `appliance`, `seen`) VALUES
(1400, 12234, 'Lower potentiometer resistance', '2023-06-13 22:45:22', 'MOTORs', 1),
(1401, 23345, 'Motor1 is drawing power even though it is switched off (Power theft)!', '2023-06-13 22:45:48', 'MOTORs', 1),
(1402, 12234, 'Lower potentiometer resistance', '2023-06-13 22:45:49', 'MOTORs', 1),
(1403, 23345, 'Lower potentiometer resistance', '2023-06-13 22:45:53', 'MOTORs', 1),
(1404, 23345, 'Motor1 is drawing power even though it is switched off (Power theft)!', '2023-06-13 22:46:19', 'MOTORs', 1),
(1405, 12234, 'Lower potentiometer resistance', '2023-06-13 22:46:22', 'MOTORs', 1),
(1406, 23345, 'Lower potentiometer resistance', '2023-06-13 22:46:25', 'MOTORs', 1),
(1407, 12234, 'Lower potentiometer resistance', '2023-06-13 22:46:46', 'MOTORs', 1),
(1408, 23345, 'Lower potentiometer resistance', '2023-06-13 22:46:50', 'MOTORs', 1),
(1409, 23345, 'Motor1 is drawing power even though it is switched off (Power theft)!', '2023-06-13 22:47:14', 'MOTORs', 1),
(1410, 12234, 'Lower potentiometer resistance', '2023-06-13 22:47:19', 'MOTORs', 1),
(1411, 23345, 'Lower potentiometer resistance', '2023-06-13 22:47:22', 'MOTORs', 1),
(1412, 12234, 'Lower potentiometer resistance', '2023-06-13 22:47:45', 'MOTORs', 1),
(1413, 12234, 'Lower potentiometer resistance', '2023-06-13 22:48:08', 'MOTORs', 1),
(1414, 23345, 'Lower potentiometer resistance', '2023-06-13 22:48:11', 'MOTORs', 1),
(1415, 12234, 'Lower potentiometer resistance', '2023-06-13 22:48:29', 'MOTORs', 1),
(1416, 23345, 'Lower potentiometer resistance', '2023-06-13 22:48:32', 'MOTORs', 1),
(1417, 12234, 'Lower potentiometer resistance', '2023-06-13 22:48:50', 'MOTORs', 1),
(1418, 23345, 'Lower potentiometer resistance', '2023-06-13 22:48:54', 'MOTORs', 1),
(1419, 12234, 'Lower potentiometer resistance', '2023-06-13 22:49:11', 'MOTORs', 1),
(1420, 23345, 'Lower potentiometer resistance', '2023-06-13 22:49:18', 'MOTORs', 1),
(1421, 12234, 'Lower potentiometer resistance', '2023-06-13 22:49:39', 'MOTORs', 1),
(1422, 23345, 'Lower potentiometer resistance', '2023-06-13 22:49:42', 'MOTORs', 1),
(1423, 12234, 'Lower potentiometer resistance', '2023-06-13 22:50:09', 'MOTORs', 1),
(1424, 23345, 'Lower potentiometer resistance', '2023-06-13 22:50:12', 'MOTORs', 1),
(1425, 12234, 'Lower potentiometer resistance', '2023-06-13 22:50:30', 'MOTORs', 1),
(1426, 23345, 'Lower potentiometer resistance', '2023-06-13 22:50:34', 'MOTORs', 1),
(1427, 12234, 'Lower potentiometer resistance', '2023-06-13 22:50:52', 'MOTORs', 1),
(1428, 23345, 'Lower potentiometer resistance', '2023-06-13 22:50:55', 'MOTORs', 1),
(1429, 12234, 'Lower potentiometer resistance', '2023-06-13 22:51:21', 'MOTORs', 1),
(1430, 12234, 'Lower potentiometer resistance', '2023-06-13 22:51:53', 'MOTORs', 1),
(1431, 23345, 'Lower potentiometer resistance', '2023-06-13 22:52:05', 'MOTORs', 1),
(1432, 12234, 'Lower potentiometer resistance', '2023-06-13 22:52:38', 'MOTORs', 1),
(1433, 23345, 'Lower potentiometer resistance', '2023-06-13 22:52:42', 'MOTORs', 1),
(1434, 12234, 'Lower potentiometer resistance', '2023-06-13 22:53:04', 'MOTORs', 1),
(1435, 23345, 'Lower potentiometer resistance', '2023-06-13 22:53:08', 'MOTORs', 1),
(1436, 12234, 'Lower potentiometer resistance', '2023-06-13 22:53:26', 'MOTORs', 1),
(1437, 23345, 'Lower potentiometer resistance', '2023-06-13 22:53:29', 'MOTORs', 1),
(1438, 12234, 'Lower potentiometer resistance', '2023-06-13 22:53:51', 'MOTORs', 1),
(1439, 23345, 'Lower potentiometer resistance', '2023-06-13 22:53:55', 'MOTORs', 1),
(1440, 12234, 'Lower potentiometer resistance', '2023-06-13 22:54:13', 'MOTORs', 1),
(1441, 23345, 'Lower potentiometer resistance', '2023-06-13 22:54:17', 'MOTORs', 1),
(1442, 12234, 'Lower potentiometer resistance', '2023-06-13 22:54:38', 'MOTORs', 1),
(1443, 23345, 'Lower potentiometer resistance', '2023-06-13 22:54:41', 'MOTORs', 1),
(1444, 23345, 'Wire is down for Motor2!', '2023-06-13 22:55:01', 'MOTORs', 1),
(1445, 12234, 'Lower potentiometer resistance', '2023-06-13 22:55:02', 'MOTORs', 1),
(1446, 23345, 'Lower potentiometer resistance', '2023-06-13 22:55:06', 'MOTORs', 1),
(1447, 12234, 'Lower potentiometer resistance', '2023-06-13 22:55:24', 'MOTORs', 1),
(1448, 23345, 'Lower potentiometer resistance', '2023-06-13 22:55:27', 'MOTORs', 1),
(1449, 12234, 'Lower potentiometer resistance', '2023-06-13 22:55:45', 'MOTORs', 1),
(1450, 23345, 'Lower potentiometer resistance', '2023-06-13 22:55:48', 'MOTORs', 1),
(1451, 12234, 'Lower potentiometer resistance', '2023-06-13 22:56:11', 'MOTORs', 1),
(1452, 23345, 'Lower potentiometer resistance', '2023-06-13 22:56:14', 'MOTORs', 1),
(1453, 12234, 'Lower potentiometer resistance', '2023-06-13 22:56:32', 'MOTORs', 1),
(1454, 23345, 'Lower potentiometer resistance', '2023-06-13 22:56:36', 'MOTORs', 1),
(1455, 12234, 'Lower potentiometer resistance', '2023-06-13 22:56:54', 'MOTORs', 1),
(1456, 23345, 'Lower potentiometer resistance', '2023-06-13 22:56:58', 'MOTORs', 1),
(1457, 12234, 'Lower potentiometer resistance', '2023-06-13 22:57:17', 'MOTORs', 1),
(1458, 23345, 'Lower potentiometer resistance', '2023-06-13 22:57:20', 'MOTORs', 1),
(1459, 12234, 'Lower potentiometer resistance', '2023-06-13 22:57:46', 'MOTORs', 1),
(1460, 23345, 'Lower potentiometer resistance', '2023-06-13 22:57:49', 'MOTORs', 1),
(1461, 12234, 'Lower potentiometer resistance', '2023-06-13 22:58:07', 'MOTORs', 1),
(1462, 23345, 'Lower potentiometer resistance', '2023-06-13 22:58:11', 'MOTORs', 1),
(1463, 12234, 'Lower potentiometer resistance', '2023-06-13 22:58:29', 'MOTORs', 1),
(1464, 23345, 'Lower potentiometer resistance', '2023-06-13 22:58:32', 'MOTORs', 1),
(1465, 12234, 'Lower potentiometer resistance', '2023-06-13 22:58:50', 'MOTORs', 1),
(1466, 23345, 'Lower potentiometer resistance', '2023-06-13 22:58:53', 'MOTORs', 1),
(1467, 12234, 'Lower potentiometer resistance', '2023-06-13 22:59:12', 'MOTORs', 1),
(1468, 23345, 'Lower potentiometer resistance', '2023-06-13 22:59:15', 'MOTORs', 1),
(1469, 12234, 'Lower potentiometer resistance', '2023-06-13 22:59:37', 'MOTORs', 1),
(1470, 23345, 'Lower potentiometer resistance', '2023-06-13 22:59:40', 'MOTORs', 1),
(1471, 12234, 'Lower potentiometer resistance', '2023-06-13 23:00:02', 'MOTORs', 1),
(1472, 23345, 'Lower potentiometer resistance', '2023-06-13 23:00:06', 'MOTORs', 1),
(1473, 12234, 'Lower potentiometer resistance', '2023-06-13 23:00:23', 'MOTORs', 1),
(1474, 23345, 'Lower potentiometer resistance', '2023-06-13 23:00:27', 'MOTORs', 1),
(1475, 12234, 'Lower potentiometer resistance', '2023-06-13 23:00:44', 'MOTORs', 1),
(1476, 23345, 'Lower potentiometer resistance', '2023-06-13 23:00:48', 'MOTORs', 1),
(1477, 12234, 'Wire is down for LE2!', '2023-06-13 23:00:59', 'LEDs', 1),
(1478, 12234, 'Wire is down for Motor2!', '2023-06-13 23:01:06', 'MOTORs', 1),
(1479, 23345, 'Wire is down for Motor2!', '2023-06-13 23:01:07', 'MOTORs', 1),
(1480, 12234, 'Lower potentiometer resistance', '2023-06-13 23:01:09', 'MOTORs', 1),
(1481, 23345, 'Lower potentiometer resistance', '2023-06-13 23:01:14', 'MOTORs', 1),
(1482, 12234, 'Wire is down for LE2!', '2023-06-13 23:03:56', 'LEDs', 1),
(1483, 23345, 'Wire is down for Motor2!', '2023-06-14 08:25:24', 'MOTORs', 1),
(1484, 23345, 'Lower potentiometer resistance', '2023-06-14 08:25:27', 'MOTORs', 1),
(1485, 23345, 'Wire is down for Motor2!', '2023-06-14 08:26:25', 'MOTORs', 1),
(1486, 23345, 'Lower potentiometer resistance', '2023-06-14 08:26:29', 'MOTORs', 1),
(1487, 23345, 'Wire is down for Motor2!', '2023-06-14 08:33:39', 'MOTORs', 1),
(1488, 23345, 'Lower potentiometer resistance', '2023-06-14 08:33:42', 'MOTORs', 1),
(1489, 12234, 'Wire is down for Motor2!', '2023-06-14 08:38:44', 'MOTORs', 1),
(1490, 12234, 'Lower potentiometer resistance', '2023-06-14 08:38:46', 'MOTORs', 1),
(1491, 12234, 'Wire is down for Motor2!', '2023-06-14 08:39:16', 'MOTORs', 1),
(1492, 12234, 'Lower potentiometer resistance', '2023-06-14 08:39:18', 'MOTORs', 1),
(1493, 12234, 'Wire is down for Motor2!', '2023-06-14 08:39:52', 'MOTORs', 1),
(1494, 12234, 'Lower potentiometer resistance', '2023-06-14 08:39:53', 'MOTORs', 1),
(1495, 23345, 'Wire is down for LED!', '2023-06-14 08:40:26', 'LEDs', 1),
(1496, 12234, 'Wire is down for LE2!', '2023-06-14 08:41:51', 'LEDs', 1),
(1497, 12234, 'Wire is down for LE2!', '2023-06-14 08:42:06', 'LEDs', 1),
(1498, 12234, 'Wire is down for Motor2!', '2023-06-14 08:46:13', 'MOTORs', 1),
(1499, 12234, 'Wire is down for Motor2!', '2023-06-14 08:46:47', 'MOTORs', 1),
(1500, 12234, 'Lower potentiometer resistance', '2023-06-14 08:46:49', 'MOTORs', 1),
(1501, 12234, 'Wire is down for Motor2!', '2023-06-14 08:48:50', 'MOTORs', 1),
(1502, 12234, 'Lower potentiometer resistance', '2023-06-14 08:48:53', 'MOTORs', 1),
(1503, 23345, 'Wire is down for Motor2!', '2023-06-14 08:50:46', 'MOTORs', 1),
(1504, 23345, 'Lower potentiometer resistance', '2023-06-14 08:50:49', 'MOTORs', 1),
(1505, 23345, 'Wire is down for Motor2!', '2023-06-14 08:51:41', 'MOTORs', 1),
(1506, 23345, 'Lower potentiometer resistance', '2023-06-14 08:51:44', 'MOTORs', 1),
(1507, 23345, 'Wire is down for Motor2!', '2023-06-14 08:52:09', 'MOTORs', 1),
(1508, 23345, 'Lower potentiometer resistance', '2023-06-14 08:52:13', 'MOTORs', 1),
(1509, 23345, 'Wire is down for Motor2!', '2023-06-14 08:52:41', 'MOTORs', 1),
(1510, 23345, 'Lower potentiometer resistance', '2023-06-14 08:52:45', 'MOTORs', 1),
(1511, 23345, 'Wire is down for Motor2!', '2023-06-14 08:53:13', 'MOTORs', 1),
(1512, 23345, 'Lower potentiometer resistance', '2023-06-14 08:53:17', 'MOTORs', 1),
(1513, 23345, 'Wire is down for Motor2!', '2023-06-14 08:53:43', 'MOTORs', 1),
(1514, 23345, 'Lower potentiometer resistance', '2023-06-14 08:53:46', 'MOTORs', 1),
(1515, 23345, 'Wire is down for Motor2!', '2023-06-14 08:54:13', 'MOTORs', 1),
(1516, 23345, 'Lower potentiometer resistance', '2023-06-14 08:54:17', 'MOTORs', 1),
(1517, 23345, 'Wire is down for Motor2!', '2023-06-14 08:54:46', 'MOTORs', 1),
(1518, 23345, 'Lower potentiometer resistance', '2023-06-14 08:54:50', 'MOTORs', 1),
(1519, 23345, 'Wire is down for Motor2!', '2023-06-14 08:55:12', 'MOTORs', 1),
(1520, 23345, 'Lower potentiometer resistance', '2023-06-14 08:55:16', 'MOTORs', 1),
(1521, 23345, 'Wire is down for Motor2!', '2023-06-14 08:55:44', 'MOTORs', 1),
(1522, 23345, 'Lower potentiometer resistance', '2023-06-14 08:55:47', 'MOTORs', 1),
(1523, 23345, 'Wire is down for Motor2!', '2023-06-14 08:56:16', 'MOTORs', 1),
(1524, 23345, 'Lower potentiometer resistance', '2023-06-14 08:56:20', 'MOTORs', 1),
(1525, 23345, 'Wire is down for Motor2!', '2023-06-14 08:56:48', 'MOTORs', 1),
(1526, 23345, 'Lower potentiometer resistance', '2023-06-14 08:56:51', 'MOTORs', 1),
(1527, 23345, 'Wire is down for Motor2!', '2023-06-14 08:57:24', 'MOTORs', 1),
(1528, 23345, 'Lower potentiometer resistance', '2023-06-14 08:57:28', 'MOTORs', 1),
(1529, 23345, 'Wire is down for Motor2!', '2023-06-14 08:58:01', 'MOTORs', 1),
(1530, 23345, 'Lower potentiometer resistance', '2023-06-14 08:58:06', 'MOTORs', 1),
(1531, 23345, 'Wire is down for Motor1!', '2023-06-14 08:58:37', 'MOTORs', 1),
(1532, 23345, 'Wire is down for Motor2!', '2023-06-14 08:58:38', 'MOTORs', 1),
(1533, 23345, 'Wire is down for Motor1!', '2023-06-14 08:59:27', 'MOTORs', 1),
(1534, 23345, 'Wire is down for Motor2!', '2023-06-14 08:59:29', 'MOTORs', 1),
(1535, 23345, 'Wire is down for Motor1!', '2023-06-14 09:00:11', 'MOTORs', 1),
(1536, 23345, 'Wire is down for Motor2!', '2023-06-14 09:00:12', 'MOTORs', 1),
(1537, 23345, 'Lower potentiometer resistance', '2023-06-14 09:00:16', 'MOTORs', 1),
(1538, 23345, 'Wire is down for Motor1!', '2023-06-14 09:00:48', 'MOTORs', 1),
(1539, 23345, 'Wire is down for Motor2!', '2023-06-14 09:00:50', 'MOTORs', 1),
(1540, 23345, 'Wire is down for Motor2!', '2023-06-14 09:01:33', 'MOTORs', 1),
(1541, 23345, 'Lower potentiometer resistance', '2023-06-14 09:01:37', 'MOTORs', 1),
(1542, 23345, 'Wire is down for Motor1!', '2023-06-14 09:02:08', 'MOTORs', 1),
(1543, 23345, 'Wire is down for Motor2!', '2023-06-14 09:02:10', 'MOTORs', 1),
(1544, 23345, 'Lower potentiometer resistance', '2023-06-14 09:02:14', 'MOTORs', 1),
(1545, 23345, 'Wire is down for Motor1!', '2023-06-14 09:02:49', 'MOTORs', 1),
(1546, 23345, 'Lower potentiometer resistance', '2023-06-14 09:03:00', 'MOTORs', 1),
(1547, 23345, 'Wire is down for Motor1!', '2023-06-14 09:03:28', 'MOTORs', 1),
(1548, 23345, 'Wire is down for Motor2!', '2023-06-14 09:03:30', 'MOTORs', 1),
(1549, 23345, 'Lower potentiometer resistance', '2023-06-14 09:03:34', 'MOTORs', 1),
(1550, 23345, 'Wire is down for Motor1!', '2023-06-14 09:04:19', 'MOTORs', 1),
(1551, 23345, 'Wire is down for Motor2!', '2023-06-14 09:04:21', 'MOTORs', 1),
(1552, 23345, 'Lower potentiometer resistance', '2023-06-14 09:04:25', 'MOTORs', 1),
(1553, 23345, 'Wire is down for Motor1!', '2023-06-14 09:04:58', 'MOTORs', 1),
(1554, 23345, 'Wire is down for Motor2!', '2023-06-14 09:05:00', 'MOTORs', 1),
(1555, 23345, 'Lower potentiometer resistance', '2023-06-14 09:05:05', 'MOTORs', 1),
(1556, 23345, 'Wire is down for Motor1!', '2023-06-14 09:05:37', 'MOTORs', 1),
(1557, 23345, 'Wire is down for Motor2!', '2023-06-14 09:05:39', 'MOTORs', 1),
(1558, 23345, 'Lower potentiometer resistance', '2023-06-14 09:05:43', 'MOTORs', 1),
(1559, 23345, 'Wire is down for Motor1!', '2023-06-14 09:06:14', 'MOTORs', 1),
(1560, 23345, 'Wire is down for Motor2!', '2023-06-14 09:06:16', 'MOTORs', 1),
(1561, 23345, 'Wire is down for Motor1!', '2023-06-14 09:06:49', 'MOTORs', 1),
(1562, 23345, 'Wire is down for Motor2!', '2023-06-14 09:06:51', 'MOTORs', 1),
(1563, 23345, 'Lower potentiometer resistance', '2023-06-14 09:06:54', 'MOTORs', 1),
(1564, 23345, 'Wire is down for Motor1!', '2023-06-14 09:07:19', 'MOTORs', 1),
(1565, 23345, 'Wire is down for Motor2!', '2023-06-14 09:07:26', 'MOTORs', 1),
(1566, 23345, 'Lower potentiometer resistance', '2023-06-14 09:07:29', 'MOTORs', 1),
(1567, 23345, 'Wire is down for Motor1!', '2023-06-14 09:07:49', 'MOTORs', 1),
(1568, 23345, 'Wire is down for Motor2!', '2023-06-14 09:07:51', 'MOTORs', 1),
(1569, 23345, 'Lower potentiometer resistance', '2023-06-14 09:07:55', 'MOTORs', 1),
(1570, 23345, 'Wire is down for Motor1!', '2023-06-14 09:08:18', 'MOTORs', 1),
(1571, 23345, 'Wire is down for Motor2!', '2023-06-14 09:08:19', 'MOTORs', 1),
(1572, 23345, 'Lower potentiometer resistance', '2023-06-14 09:08:23', 'MOTORs', 1),
(1573, 23345, 'Motor1 is drawing power even though it is switched off (Power theft)!', '2023-06-14 09:11:55', 'MOTORs', 1),
(1574, 23345, 'Motor1 is drawing power even though it is switched off (Power theft)!', '2023-06-14 09:12:17', 'MOTORs', 1),
(1575, 12234, 'Wire is down for Motor2!', '2023-06-14 10:31:02', 'MOTORs', 0),
(1576, 12234, 'Lower potentiometer resistance', '2023-06-14 10:31:03', 'MOTORs', 0),
(1577, 12234, 'Wire is down for Motor2!', '2023-06-14 10:31:23', 'MOTORs', 0),
(1578, 12234, 'Lower potentiometer resistance', '2023-06-14 10:31:25', 'MOTORs', 0),
(1579, 12234, 'Wire is down for Motor2!', '2023-06-14 10:31:48', 'MOTORs', 0),
(1580, 12234, 'Lower potentiometer resistance', '2023-06-14 10:31:49', 'MOTORs', 0),
(1581, 12234, 'Wire is down for Motor2!', '2023-06-14 10:32:10', 'MOTORs', 0),
(1582, 12234, 'Lower potentiometer resistance', '2023-06-14 10:32:12', 'MOTORs', 0),
(1583, 12234, 'Wire is down for Motor2!', '2023-06-14 10:32:32', 'MOTORs', 0),
(1584, 12234, 'Lower potentiometer resistance', '2023-06-14 10:32:34', 'MOTORs', 0),
(1585, 12234, 'Wire is down for Motor2!', '2023-06-14 10:32:55', 'MOTORs', 0),
(1586, 12234, 'Lower potentiometer resistance', '2023-06-14 10:32:56', 'MOTORs', 0),
(1587, 12234, 'Wire is down for Motor2!', '2023-06-14 10:33:16', 'MOTORs', 0),
(1588, 12234, 'Lower potentiometer resistance', '2023-06-14 10:33:18', 'MOTORs', 0),
(1589, 12234, 'Wire is down for Motor2!', '2023-06-14 10:33:39', 'MOTORs', 0),
(1590, 12234, 'Lower potentiometer resistance', '2023-06-14 10:33:40', 'MOTORs', 0),
(1591, 12234, 'Wire is down for Motor2!', '2023-06-14 10:34:02', 'MOTORs', 0),
(1592, 12234, 'Lower potentiometer resistance', '2023-06-14 10:34:04', 'MOTORs', 0),
(1593, 12234, 'Wire is down for Motor2!', '2023-06-14 10:34:24', 'MOTORs', 0),
(1594, 12234, 'Lower potentiometer resistance', '2023-06-14 10:34:26', 'MOTORs', 0),
(1595, 12234, 'Wire is down for Motor2!', '2023-06-14 10:34:46', 'MOTORs', 0),
(1596, 12234, 'Lower potentiometer resistance', '2023-06-14 10:34:47', 'MOTORs', 0),
(1597, 12234, 'Wire is down for Motor2!', '2023-06-14 10:35:08', 'MOTORs', 0),
(1598, 12234, 'Lower potentiometer resistance', '2023-06-14 10:35:10', 'MOTORs', 0),
(1599, 12234, 'Wire is down for Motor2!', '2023-06-14 10:35:31', 'MOTORs', 0),
(1600, 12234, 'Lower potentiometer resistance', '2023-06-14 10:35:32', 'MOTORs', 0),
(1601, 12234, 'Wire is down for Motor2!', '2023-06-14 10:35:53', 'MOTORs', 0),
(1602, 12234, 'Lower potentiometer resistance', '2023-06-14 10:35:54', 'MOTORs', 0),
(1603, 12234, 'Wire is down for Motor2!', '2023-06-14 10:36:18', 'MOTORs', 0),
(1604, 12234, 'Lower potentiometer resistance', '2023-06-14 10:36:20', 'MOTORs', 0),
(1605, 12234, 'Wire is down for Motor2!', '2023-06-14 10:36:40', 'MOTORs', 0),
(1606, 12234, 'Lower potentiometer resistance', '2023-06-14 10:36:42', 'MOTORs', 0),
(1607, 12234, 'Wire is down for Motor2!', '2023-06-14 10:37:01', 'MOTORs', 0),
(1608, 12234, 'Lower potentiometer resistance', '2023-06-14 10:37:03', 'MOTORs', 0),
(1609, 12234, 'Wire is down for Motor2!', '2023-06-14 10:37:24', 'MOTORs', 0),
(1610, 12234, 'Lower potentiometer resistance', '2023-06-14 10:37:25', 'MOTORs', 0),
(1611, 12234, 'Wire is down for Motor2!', '2023-06-14 10:37:48', 'MOTORs', 0),
(1612, 12234, 'Lower potentiometer resistance', '2023-06-14 10:37:49', 'MOTORs', 0),
(1613, 12234, 'Wire is down for Motor2!', '2023-06-14 10:38:10', 'MOTORs', 0),
(1614, 12234, 'Lower potentiometer resistance', '2023-06-14 10:38:12', 'MOTORs', 0),
(1615, 12234, 'Wire is down for Motor2!', '2023-06-14 10:38:33', 'MOTORs', 0),
(1616, 12234, 'Lower potentiometer resistance', '2023-06-14 10:38:35', 'MOTORs', 0),
(1617, 12234, 'Wire is down for Motor2!', '2023-06-14 10:38:55', 'MOTORs', 0),
(1618, 23345, 'Motor1 is drawing power even though it is switched off (Power theft)!', '2023-06-14 10:38:57', 'MOTORs', 0),
(1619, 12234, 'Lower potentiometer resistance', '2023-06-14 10:38:59', 'MOTORs', 0),
(1620, 12234, 'Wire is down for Motor2!', '2023-06-14 10:39:20', 'MOTORs', 0),
(1621, 23345, 'Motor1 is drawing power even though it is switched off (Power theft)!', '2023-06-14 10:39:22', 'MOTORs', 0),
(1622, 12234, 'Lower potentiometer resistance', '2023-06-14 10:39:23', 'MOTORs', 0),
(1623, 12234, 'Wire is down for Motor2!', '2023-06-14 10:39:44', 'MOTORs', 0),
(1624, 12234, 'Lower potentiometer resistance', '2023-06-14 10:39:46', 'MOTORs', 0),
(1625, 12234, 'Wire is down for Motor2!', '2023-06-14 10:40:05', 'MOTORs', 0),
(1626, 12234, 'Lower potentiometer resistance', '2023-06-14 10:40:07', 'MOTORs', 0),
(1627, 12234, 'Wire is down for Motor2!', '2023-06-14 10:40:28', 'MOTORs', 0),
(1628, 12234, 'Lower potentiometer resistance', '2023-06-14 10:40:30', 'MOTORs', 0),
(1629, 12234, 'Wire is down for Motor2!', '2023-06-14 10:40:50', 'MOTORs', 0),
(1630, 12234, 'Lower potentiometer resistance', '2023-06-14 10:40:51', 'MOTORs', 0),
(1631, 12234, 'Wire is down for Motor2!', '2023-06-14 10:41:13', 'MOTORs', 0),
(1632, 12234, 'Lower potentiometer resistance', '2023-06-14 10:41:14', 'MOTORs', 0),
(1633, 12234, 'Wire is down for Motor2!', '2023-06-14 10:41:35', 'MOTORs', 0),
(1634, 12234, 'Lower potentiometer resistance', '2023-06-14 10:41:37', 'MOTORs', 0),
(1635, 12234, 'Lower potentiometer resistance', '2023-06-14 10:42:51', 'MOTORs', 0),
(1636, 12234, 'Wire is down for Motor2!', '2023-06-14 10:43:12', 'MOTORs', 0),
(1637, 12234, 'Lower potentiometer resistance', '2023-06-14 10:43:13', 'MOTORs', 0),
(1638, 12234, 'Wire is down for Motor2!', '2023-06-14 10:43:34', 'MOTORs', 0),
(1639, 12234, 'Lower potentiometer resistance', '2023-06-14 10:43:35', 'MOTORs', 0),
(1640, 12234, 'Wire is down for Motor2!', '2023-06-14 10:43:57', 'MOTORs', 0),
(1641, 12234, 'Lower potentiometer resistance', '2023-06-14 10:43:58', 'MOTORs', 0),
(1642, 12234, 'Wire is down for Motor2!', '2023-06-14 10:44:18', 'MOTORs', 0),
(1643, 12234, 'Lower potentiometer resistance', '2023-06-14 10:44:20', 'MOTORs', 0),
(1644, 12234, 'Wire is down for Motor2!', '2023-06-14 10:44:41', 'MOTORs', 0),
(1645, 12234, 'Lower potentiometer resistance', '2023-06-14 10:44:43', 'MOTORs', 0),
(1646, 12234, 'Wire is down for Motor2!', '2023-06-14 10:45:03', 'MOTORs', 0),
(1647, 12234, 'Lower potentiometer resistance', '2023-06-14 10:45:04', 'MOTORs', 0),
(1648, 12234, 'Wire is down for Motor2!', '2023-06-14 10:45:25', 'MOTORs', 0),
(1649, 12234, 'Lower potentiometer resistance', '2023-06-14 10:45:26', 'MOTORs', 0),
(1650, 12234, 'Wire is down for Motor2!', '2023-06-14 10:45:47', 'MOTORs', 0),
(1651, 12234, 'Lower potentiometer resistance', '2023-06-14 10:45:49', 'MOTORs', 0),
(1652, 12234, 'Wire is down for Motor2!', '2023-06-14 10:46:09', 'MOTORs', 0),
(1653, 12234, 'Lower potentiometer resistance', '2023-06-14 10:46:10', 'MOTORs', 0),
(1654, 12234, 'Wire is down for Motor2!', '2023-06-14 10:46:31', 'MOTORs', 0),
(1655, 12234, 'Lower potentiometer resistance', '2023-06-14 10:46:32', 'MOTORs', 0),
(1656, 12234, 'Wire is down for Motor2!', '2023-06-14 10:46:53', 'MOTORs', 0),
(1657, 12234, 'Lower potentiometer resistance', '2023-06-14 10:46:55', 'MOTORs', 0),
(1658, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:47:04', 'LEDs', 0),
(1659, 12234, 'Wire is down for Motor2!', '2023-06-14 10:47:17', 'MOTORs', 0),
(1660, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:47:18', 'LEDs', 0),
(1661, 12234, 'Lower potentiometer resistance', '2023-06-14 10:47:18', 'MOTORs', 0),
(1662, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:47:31', 'LEDs', 0),
(1663, 12234, 'Wire is down for Motor2!', '2023-06-14 10:47:39', 'MOTORs', 0),
(1664, 12234, 'Lower potentiometer resistance', '2023-06-14 10:47:40', 'MOTORs', 0),
(1665, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:47:45', 'LEDs', 0),
(1666, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:47:59', 'LEDs', 0),
(1667, 12234, 'Wire is down for Motor2!', '2023-06-14 10:48:01', 'MOTORs', 0),
(1668, 12234, 'Lower potentiometer resistance', '2023-06-14 10:48:03', 'MOTORs', 0),
(1669, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:48:13', 'LEDs', 0),
(1670, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:48:24', 'LEDs', 0),
(1671, 12234, 'Wire is down for Motor2!', '2023-06-14 10:48:25', 'MOTORs', 0),
(1672, 12234, 'Lower potentiometer resistance', '2023-06-14 10:48:26', 'MOTORs', 0),
(1673, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:48:39', 'LEDs', 0),
(1674, 12234, 'Wire is down for Motor2!', '2023-06-14 10:48:46', 'MOTORs', 0),
(1675, 12234, 'Lower potentiometer resistance', '2023-06-14 10:48:47', 'MOTORs', 0),
(1676, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:48:53', 'LEDs', 0),
(1677, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:49:06', 'LEDs', 0),
(1678, 12234, 'Wire is down for Motor2!', '2023-06-14 10:49:07', 'MOTORs', 0),
(1679, 12234, 'Lower potentiometer resistance', '2023-06-14 10:49:08', 'MOTORs', 0),
(1680, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:49:18', 'LEDs', 0),
(1681, 12234, 'Wire is down for Motor2!', '2023-06-14 10:49:30', 'MOTORs', 0),
(1682, 12234, 'Lower potentiometer resistance', '2023-06-14 10:49:31', 'MOTORs', 0),
(1683, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:49:34', 'LEDs', 0),
(1684, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:49:48', 'LEDs', 0),
(1685, 12234, 'Wire is down for Motor2!', '2023-06-14 10:49:52', 'MOTORs', 0),
(1686, 12234, 'Lower potentiometer resistance', '2023-06-14 10:49:53', 'MOTORs', 0),
(1687, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:50:01', 'LEDs', 0),
(1688, 12234, 'Wire is down for Motor2!', '2023-06-14 10:50:14', 'MOTORs', 0),
(1689, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:50:14', 'LEDs', 0),
(1690, 12234, 'Lower potentiometer resistance', '2023-06-14 10:50:16', 'MOTORs', 0),
(1691, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:50:28', 'LEDs', 0),
(1692, 12234, 'Wire is down for Motor2!', '2023-06-14 10:50:36', 'MOTORs', 0),
(1693, 12234, 'Lower potentiometer resistance', '2023-06-14 10:50:37', 'MOTORs', 0),
(1694, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:50:41', 'LEDs', 0),
(1695, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:50:54', 'LEDs', 0),
(1696, 12234, 'Wire is down for Motor2!', '2023-06-14 10:50:58', 'MOTORs', 0),
(1697, 12234, 'Lower potentiometer resistance', '2023-06-14 10:51:00', 'MOTORs', 0),
(1698, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:51:22', 'LEDs', 0),
(1699, 12234, 'Wire is down for Motor2!', '2023-06-14 10:51:28', 'MOTORs', 0),
(1700, 12234, 'Lower potentiometer resistance', '2023-06-14 10:51:29', 'MOTORs', 0),
(1701, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:51:35', 'LEDs', 0),
(1702, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:51:48', 'LEDs', 0),
(1703, 12234, 'Wire is down for Motor2!', '2023-06-14 10:51:49', 'MOTORs', 0),
(1704, 12234, 'Lower potentiometer resistance', '2023-06-14 10:51:51', 'MOTORs', 0),
(1705, 23345, 'Decrease resistance for LEDs Potentiometer', '2023-06-14 10:52:02', 'LEDs', 0),
(1706, 12234, 'Wire is down for Motor2!', '2023-06-14 10:52:11', 'MOTORs', 0),
(1707, 12234, 'Lower potentiometer resistance', '2023-06-14 10:52:12', 'MOTORs', 0),
(1708, 12234, 'Wire is down for Motor2!', '2023-06-14 10:53:46', 'MOTORs', 0),
(1709, 12234, 'Lower potentiometer resistance', '2023-06-14 10:53:47', 'MOTORs', 0),
(1710, 12234, 'Wire is down for Motor2!', '2023-06-14 10:54:20', 'MOTORs', 0),
(1711, 23345, 'Wire is down for Motor1!', '2023-06-14 10:54:22', 'MOTORs', 0),
(1712, 23345, 'Wire is down for Motor2!', '2023-06-14 10:54:26', 'MOTORs', 0),
(1713, 12234, 'Lower potentiometer resistance', '2023-06-14 10:54:28', 'MOTORs', 0),
(1714, 12234, 'Wire is down for Motor2!', '2023-06-14 10:56:04', 'MOTORs', 0),
(1715, 23345, 'Wire is down for Motor1!', '2023-06-14 10:56:05', 'MOTORs', 0),
(1716, 23345, 'Wire is down for Motor2!', '2023-06-14 10:56:07', 'MOTORs', 0),
(1717, 12234, 'Lower potentiometer resistance', '2023-06-14 10:56:09', 'MOTORs', 0);

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `userid` int(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(20) NOT NULL,
  `user_type` varchar(10) NOT NULL,
  `channel_id` varchar(100) NOT NULL,
  `field_no` int(20) NOT NULL,
  `Read_Api` varchar(100) NOT NULL,
  `Write_Api` varchar(100) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp(),
  `priority` text NOT NULL DEFAULT '1234'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`userid`, `username`, `email`, `password`, `user_type`, `channel_id`, `field_no`, `Read_Api`, `Write_Api`, `date`, `priority`) VALUES
(12234, 'Resident1', 'Resident1@students.iiit.ac.in', 'password1', 'resident', '2165368', 6, 'EFISS04IFA6364N9', '899FMRYW1H2FPCNJ', '2023-05-27', '12'),
(23345, 'Resident2', 'Resident2@students.iiit.ac.in', 'password2', 'resident', '2165370', 7, 'D3LNELVJ4YHFILVP', 'RLEHO8H1Z8C0I48Y', '2023-05-27', '21'),
(91507, 'admin', 'admin@students.iiit.ac.in', 'admin', 'admin', '2165368,2165370', 13, 'EFISS04IFA6364N9,D3LNELVJ4YHFILVP', '899FMRYW1H2FPCNJ,RLEHO8H1Z8C0I48Y', '2023-05-29', '1234');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Notifications`
--
ALTER TABLE `Notifications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`userid`),
  ADD UNIQUE KEY `userid_2` (`userid`),
  ADD KEY `userid` (`userid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Notifications`
--
ALTER TABLE `Notifications`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1718;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
