-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 04, 2024 at 07:46 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `testdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `employee_id` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `contactnumber` varchar(15) NOT NULL,
  `email` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `profile_image` varchar(255) DEFAULT NULL,
  `is_super_admin` tinyint(1) DEFAULT 0,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `password_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `employee_id`, `lastname`, `firstname`, `contactnumber`, `email`, `created_at`, `profile_image`, `is_super_admin`, `deleted_at`, `password_id`) VALUES
(16, 'SUM2021-003666', 'Pelaez', 'Luis', '09764274590', 'e.luis.pelaez@gmail.com', '2024-12-03 23:08:21', NULL, 1, NULL, 16),
(17, 'SLU-29485', 'Angelo', 'Shem', '09764729450', 'shemangelo@gmail.com', '2024-12-03 23:17:11', '4M.jpeg', 0, NULL, 17);

-- --------------------------------------------------------

--
-- Table structure for table `admin_activity_log`
--

CREATE TABLE `admin_activity_log` (
  `activity_id` int(11) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `activity_type` varchar(255) NOT NULL,
  `activity_timestamp` datetime NOT NULL,
  `details` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_activity_log`
--

INSERT INTO `admin_activity_log` (`activity_id`, `admin_id`, `activity_type`, `activity_timestamp`, `details`, `created_at`) VALUES
(200, 16, 'Login successful', '2024-12-03 23:10:11', 'Login successful - User ID: 16', '2024-12-03 23:10:11'),
(201, 16, 'Login successful', '2024-12-03 23:16:44', 'Login successful - User ID: 16', '2024-12-03 23:16:44'),
(202, 16, 'Added new admin', '2024-12-03 23:17:11', 'Added new admin - User ID: 16', '2024-12-03 23:17:11'),
(203, 16, 'Toggled Super Admin Status for admin 17', '2024-12-03 23:17:22', 'Toggled Super Admin Status for admin 17 - User ID: 16', '2024-12-03 23:17:22'),
(204, 16, 'Toggled Super Admin Status for admin 17', '2024-12-03 23:17:28', 'Toggled Super Admin Status for admin 17 - User ID: 16', '2024-12-03 23:17:28'),
(205, 16, 'Login successful', '2024-12-03 23:31:49', 'Login successful - User ID: 16', '2024-12-03 23:31:49'),
(206, 16, 'Login successful', '2024-12-04 00:04:57', 'Login successful - User ID: 16', '2024-12-04 00:04:57'),
(207, 16, 'Login successful', '2024-12-04 01:15:22', 'Login successful - User ID: 16', '2024-12-04 01:15:22'),
(208, 16, 'Login successful', '2024-12-04 02:21:18', 'Login successful - User ID: 16', '2024-12-04 02:21:18'),
(209, 16, 'Login successful', '2024-12-04 02:28:07', 'Login successful - User ID: 16', '2024-12-04 02:28:07'),
(210, 16, 'Login successful', '2024-12-04 02:44:25', 'Login successful - User ID: 16', '2024-12-04 02:44:25'),
(211, 16, 'Login successful', '2024-12-04 15:40:54', 'Login successful - User ID: 16', '2024-12-04 15:40:54'),
(212, 16, 'Login successful', '2024-12-04 21:26:48', 'Login successful - User ID: 16', '2024-12-04 21:26:48'),
(213, 16, 'Login successful', '2024-12-04 23:20:52', 'Login successful - User ID: 16', '2024-12-04 23:20:52'),
(214, 16, 'Login successful', '2024-12-04 23:26:15', 'Login successful - User ID: 16', '2024-12-04 23:26:15'),
(215, 16, 'Login successful', '2024-12-05 02:40:44', 'Login successful - User ID: 16', '2024-12-05 02:40:44'),
(216, 16, 'Login successful', '2024-12-05 02:43:16', 'Login successful - User ID: 16', '2024-12-05 02:43:16');

-- --------------------------------------------------------

--
-- Table structure for table `passwords`
--

CREATE TABLE `passwords` (
  `password_id` int(11) NOT NULL,
  `password_hash` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `passwords`
--

INSERT INTO `passwords` (`password_id`, `password_hash`) VALUES
(15, 'scrypt:32768:8:1$6L0xm2c7dvBLmkYZ$f21a940d78a9eb94d5f21e66cf5e9dbceec77d4dfb9519501dfe08ac77090f506d1756d05a08a1784188814e8ad85785dfbcaa30082ea2bdee9d7cc1d2863530'),
(16, 'scrypt:32768:8:1$6L0xm2c7dvBLmkYZ$f21a940d78a9eb94d5f21e66cf5e9dbceec77d4dfb9519501dfe08ac77090f506d1756d05a08a1784188814e8ad85785dfbcaa30082ea2bdee9d7cc1d2863530'),
(17, 'scrypt:32768:8:1$SzMZ0ywB3ydIn8JS$73f12324aaa78ce8937f8a1d226d9eb13adc1899f466ebcca657ca6401aea9c12c7d7828cddb94fba7487276b2f76e313658727800ac50add84a53c3c0ab90cc'),
(18, 'scrypt:32768:8:1$Mzm7PrBV3kOWyMXY$15991628d9001a992345ba83bb94d9ff4ba39d0d63bab729d2d1d4e928521b74c3497129bc552dcce47d726a0e1fc677aff9b7b1257f845abe54aa8939766b9a'),
(19, 'scrypt:32768:8:1$VvJWT1Hr6IB8igqN$20f8984dace76e48a2fa2447fb4ffd675ce45f54f9ce71363d22f1ac7f013284c903f64f540834fac77e89d6fc9495ada5908cb138a46a576fa205aa042db1b9'),
(20, 'scrypt:32768:8:1$1xaQCVjuNN3ZesAl$eaa1685c0fc69eaaa2c1440f80ad5b7d50fe2740cd7baa02f0386ac1e5ff01c98581383f007cf5502288e1b1a35d2a21d8f3e62b7f9f1c5613783eb9c940744d'),
(21, 'scrypt:32768:8:1$8ev7r0i9NUXLzDhw$e70201587bcffcc13a388c1dae20e58e150f82e987a87c226053408c133f5bbfc6d47413340d49594d930a439b28f0136578902f161edbb97b215a191f1a2ff4'),
(22, 'scrypt:32768:8:1$gLGeCcnF0Pbc2jw6$d5745b9f4604edfa8bb41d0fb7998233ae4f61d7d4ae2ea7126cbe5adc7949922b09bebb36bad11f040b2c6e6a69bb72f8e24f212ac38f1d03143eb545adf521'),
(23, 'scrypt:32768:8:1$18rFUXUU8B9XlJme$f72f9d9ca6306d5d4aaf8342a5f7108842d0b4fecee289d00237c2fbf022417a0993a75cff3cc2e80b5b4512a39823f740b1889f560f5f1f64be219b2227eed2'),
(24, 'scrypt:32768:8:1$UArqlaRB6rWOizXr$2269c70bd972064da033384a31f17353abe16e1d57e95d3b45f0d34a3fe4ae0b1127874d8c75c5c1465aeb41e909fc292f356640b9ccf437031a324f828da8f0'),
(25, 'scrypt:32768:8:1$Cq19X5ljMQ7nGsoE$ec35aa99364d2a44f530dd8046fe45991383de273f2b6c391a0b90734051f84ce6b92a6d98a898cb21c640641d58be17b433a70f81fec4d86323a552c8e1e5dc'),
(26, 'scrypt:32768:8:1$ugBCkrozoiZSV0s0$18907d1c76553b5a02410d7e35de6b6dabb23ce9f0276428b67b224b19a9c1114a1102c5b507d5dfe2ce36c38f6ba51931cdab680d83ef86c50823584ac77421');

-- --------------------------------------------------------

--
-- Table structure for table `rfid`
--

CREATE TABLE `rfid` (
  `rfid_id` int(11) NOT NULL,
  `rfid_no` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rfid`
--

INSERT INTO `rfid` (`rfid_id`, `rfid_no`, `created_at`) VALUES
(117, '0010605475', '2024-12-03 00:36:54'),
(118, '0004250133', '2024-12-04 23:05:51'),
(119, '0004669639', '2024-12-04 23:08:32'),
(120, '0004290568', '2024-12-04 23:10:13'),
(121, '0005398438', '2024-12-04 23:12:21'),
(122, '0010571220', '2024-12-04 23:13:43'),
(123, '0010559824', '2024-12-04 23:14:49'),
(125, '0004724929', '2024-12-04 23:18:24'),
(126, '0011238051', '2024-12-04 23:20:39');

-- --------------------------------------------------------

--
-- Table structure for table `time_logs`
--

CREATE TABLE `time_logs` (
  `log_id` int(11) NOT NULL,
  `vehicle_id` int(11) NOT NULL,
  `rfid_id` int(11) NOT NULL,
  `time_in` datetime NOT NULL,
  `time_out` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `admin_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `time_logs`
--

INSERT INTO `time_logs` (`log_id`, `vehicle_id`, `rfid_id`, `time_in`, `time_out`, `created_at`, `admin_id`) VALUES
(96, 116, 126, '2024-12-05 02:00:31', '2024-12-05 02:34:39', '2024-12-05 02:00:31', 16),
(97, 108, 118, '2024-12-05 02:02:35', '2024-12-05 02:34:08', '2024-12-05 02:02:35', 16),
(99, 107, 117, '2024-12-05 02:26:33', NULL, '2024-12-05 02:26:33', 16),
(100, 115, 125, '2024-12-05 02:34:37', NULL, '2024-12-05 02:34:37', 16),
(101, 109, 119, '2024-12-05 02:34:43', NULL, '2024-12-05 02:34:43', 16);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `emp_no` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `contactnumber` varchar(15) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `profile_image` varchar(255) DEFAULT NULL,
  `is_approved` tinyint(1) NOT NULL DEFAULT 0,
  `password_id` int(11) NOT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `emp_no`, `lastname`, `firstname`, `email`, `contactnumber`, `created_at`, `profile_image`, `is_approved`, `password_id`, `deleted_at`, `updated_at`) VALUES
(66, 'SUM2021-00366', 'Pelaez', 'Luis', 'e.luis@gmail.com', '09661970287', '2024-12-03 00:36:54', 'ba49f9c9.jpeg', 1, 15, NULL, '2024-12-04 23:29:53'),
(67, 'WUP-209304', 'Puyat', 'Yuri', 'yuripuyat@gmail.com', '09748274590', '2024-12-04 23:05:51', '47b4baff.jpeg', 1, 18, NULL, '2024-12-05 00:15:53'),
(68, 'SUM2020-29495', 'Manapol', 'Patrick', 'patrickmanapol@gmail.com', '09764274859', '2024-12-04 23:08:32', '185e39fe.jpeg', 1, 19, NULL, '2024-12-05 00:15:54'),
(69, 'GB-928842', 'Angelo', 'Shem', 'shemangeloo@gmail.com', '09764285924', '2024-12-04 23:10:13', 'a699f400.jpeg', 0, 20, NULL, '2024-12-04 23:10:13'),
(70, 'GB-249895', 'Sandoval', 'Hans', 'hansmyidol@gmail.com', '09764829458', '2024-12-04 23:12:21', '392654a6.jpeg', 0, 21, NULL, '2024-12-04 23:12:21'),
(71, 'GB-923894', 'Laygo', 'Ro-eh Israel', 'grimboys@gmail.com', '09748259353', '2024-12-04 23:13:43', '2e0bd957.jpeg', 0, 22, NULL, '2024-12-04 23:13:43'),
(72, 'CAB-29382', 'Facundo', 'Ford', 'fordmyninja@gmail.com', '09764284952', '2024-12-04 23:14:49', 'adf3f364.jpeg', 1, 23, NULL, '2024-12-05 00:15:07'),
(74, 'SUM2021-284985', 'Cucio', 'Julian', 'juliancyberpunk@gmail.com', '09748429452', '2024-12-04 23:18:24', '3bdbb854.jpeg', 1, 25, NULL, '2024-12-05 00:15:49'),
(75, 'GTC-02930', 'Abrera', 'Juliecca', 'juliecaca@gmail.com', '09764274582', '2024-12-04 23:20:39', 'd0b933e2.jpg', 1, 26, NULL, '2024-12-04 23:30:02');

-- --------------------------------------------------------

--
-- Table structure for table `user_activity_log`
--

CREATE TABLE `user_activity_log` (
  `activity_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `activity_type` varchar(255) NOT NULL,
  `activity_timestamp` datetime NOT NULL,
  `details` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_activity_log`
--

INSERT INTO `user_activity_log` (`activity_id`, `user_id`, `activity_type`, `activity_timestamp`, `details`, `created_at`) VALUES
(199, 66, 'Login successful', '2024-12-03 01:49:19', 'Login successful - User ID: 66', '2024-12-03 01:49:19'),
(200, 66, 'Login successful', '2024-12-03 22:58:49', 'Login successful - User ID: 66', '2024-12-03 22:58:49'),
(201, 66, 'Login successful', '2024-12-03 23:01:21', 'Login successful - User ID: 66', '2024-12-03 23:01:21'),
(202, 66, 'Login successful', '2024-12-04 15:05:26', 'Login successful - User ID: 66', '2024-12-04 15:05:26'),
(203, 66, 'Login successful', '2024-12-04 15:09:03', 'Login successful - User ID: 66', '2024-12-04 15:09:03'),
(204, 66, 'Login successful', '2024-12-04 15:29:20', 'Login successful - User ID: 66', '2024-12-04 15:29:20'),
(205, 66, 'Login successful', '2024-12-04 15:35:26', 'Login successful - User ID: 66', '2024-12-04 15:35:26'),
(206, 66, 'Login successful', '2024-12-04 15:37:42', 'Login successful - User ID: 66', '2024-12-04 15:37:42'),
(207, 66, 'Login successful', '2024-12-04 15:59:52', 'Login successful - User ID: 66', '2024-12-04 15:59:52'),
(208, 66, 'Login successful', '2024-12-04 16:44:30', 'Login successful - User ID: 66', '2024-12-04 16:44:30'),
(209, 66, 'Login successful', '2024-12-04 16:49:38', 'Login successful - User ID: 66', '2024-12-04 16:49:38'),
(210, 66, 'Login successful', '2024-12-04 16:51:52', 'Login successful - User ID: 66', '2024-12-04 16:51:52'),
(211, 66, 'Login successful', '2024-12-04 18:12:03', 'Login successful - User ID: 66', '2024-12-04 18:12:03'),
(212, 66, 'Login successful', '2024-12-04 18:13:48', 'Login successful - User ID: 66', '2024-12-04 18:13:48'),
(213, 66, 'Login successful', '2024-12-04 18:23:18', 'Login successful - User ID: 66', '2024-12-04 18:23:18'),
(214, 66, 'Login successful', '2024-12-04 18:25:45', 'Login successful - User ID: 66', '2024-12-04 18:25:45'),
(215, 66, 'Login successful', '2024-12-04 18:29:06', 'Login successful - User ID: 66', '2024-12-04 18:29:06'),
(216, 66, 'Login successful', '2024-12-04 18:32:20', 'Login successful - User ID: 66', '2024-12-04 18:32:20'),
(217, 66, 'Login successful', '2024-12-04 18:40:40', 'Login successful - User ID: 66', '2024-12-04 18:40:40'),
(218, 66, 'Login successful', '2024-12-04 19:05:50', 'Login successful - User ID: 66', '2024-12-04 19:05:50'),
(219, 66, 'Login successful', '2024-12-04 19:07:15', 'Login successful - User ID: 66', '2024-12-04 19:07:15'),
(220, 66, 'Login successful', '2024-12-04 19:10:24', 'Login successful - User ID: 66', '2024-12-04 19:10:24'),
(221, 66, 'Login successful', '2024-12-04 19:17:38', 'Login successful - User ID: 66', '2024-12-04 19:17:38'),
(222, 66, 'Login successful', '2024-12-04 19:20:45', 'Login successful - User ID: 66', '2024-12-04 19:20:45'),
(223, 66, 'Login successful', '2024-12-04 19:24:01', 'Login successful - User ID: 66', '2024-12-04 19:24:01'),
(224, 66, 'Login successful', '2024-12-04 19:51:43', 'Login successful - User ID: 66', '2024-12-04 19:51:43'),
(225, 66, 'Login successful', '2024-12-04 19:57:13', 'Login successful - User ID: 66', '2024-12-04 19:57:13'),
(226, 66, 'Login successful', '2024-12-04 20:00:58', 'Login successful - User ID: 66', '2024-12-04 20:00:58'),
(227, 66, 'Login successful', '2024-12-04 20:03:58', 'Login successful - User ID: 66', '2024-12-04 20:03:58'),
(228, 66, 'Login successful', '2024-12-04 20:06:11', 'Login successful - User ID: 66', '2024-12-04 20:06:11'),
(229, 66, 'Login successful', '2024-12-04 20:12:22', 'Login successful - User ID: 66', '2024-12-04 20:12:22'),
(230, 66, 'Login successful', '2024-12-04 20:16:15', 'Login successful - User ID: 66', '2024-12-04 20:16:15'),
(231, 66, 'Login successful', '2024-12-04 20:17:50', 'Login successful - User ID: 66', '2024-12-04 20:17:50'),
(232, 66, 'Login successful', '2024-12-04 20:20:01', 'Login successful - User ID: 66', '2024-12-04 20:20:01'),
(233, 66, 'Login successful', '2024-12-04 20:23:05', 'Login successful - User ID: 66', '2024-12-04 20:23:05'),
(234, 66, 'Login successful', '2024-12-04 20:28:51', 'Login successful - User ID: 66', '2024-12-04 20:28:51'),
(235, 66, 'Login successful', '2024-12-04 20:31:38', 'Login successful - User ID: 66', '2024-12-04 20:31:38'),
(236, 66, 'Login successful', '2024-12-04 20:33:34', 'Login successful - User ID: 66', '2024-12-04 20:33:34'),
(237, 66, 'Login successful', '2024-12-04 20:37:45', 'Login successful - User ID: 66', '2024-12-04 20:37:45'),
(238, 66, 'Login successful', '2024-12-04 21:14:31', 'Login successful - User ID: 66', '2024-12-04 21:14:31'),
(239, 66, 'Login successful', '2024-12-04 21:18:36', 'Login successful - User ID: 66', '2024-12-04 21:18:36'),
(240, 66, 'Login successful', '2024-12-04 21:21:52', 'Login successful - User ID: 66', '2024-12-04 21:21:52'),
(241, 66, 'Login successful', '2024-12-04 21:31:41', 'Login successful - User ID: 66', '2024-12-04 21:31:41'),
(242, 66, 'Clocked In', '2024-12-05 01:27:07', 'Clocked In - User ID: 66', '2024-12-05 01:27:07'),
(243, 67, 'Clocked In', '2024-12-05 01:30:50', 'Clocked In - User ID: 67', '2024-12-05 01:30:50'),
(244, 68, 'Clocked In', '2024-12-05 01:30:53', 'Clocked In - User ID: 68', '2024-12-05 01:30:53'),
(245, 69, 'Clocked In', '2024-12-05 01:30:55', 'Clocked In - User ID: 69', '2024-12-05 01:30:55'),
(246, 70, 'Clocked In', '2024-12-05 01:30:57', 'Clocked In - User ID: 70', '2024-12-05 01:30:57'),
(247, 71, 'Clocked In', '2024-12-05 01:31:00', 'Clocked In - User ID: 71', '2024-12-05 01:31:00'),
(248, 74, 'Clocked In', '2024-12-05 01:31:25', 'Clocked In - User ID: 74', '2024-12-05 01:31:25'),
(249, 75, 'Clocked In', '2024-12-05 01:31:29', 'Clocked In - User ID: 75', '2024-12-05 01:31:29'),
(250, 66, 'Clocked In', '2024-12-05 02:00:17', 'Clocked In - User ID: 66', '2024-12-05 02:00:17'),
(251, 75, 'Clocked In', '2024-12-05 02:00:31', 'Clocked In - User ID: 75', '2024-12-05 02:00:31'),
(252, 67, 'Clocked In', '2024-12-05 02:02:35', 'Clocked In - User ID: 67', '2024-12-05 02:02:35'),
(253, 69, 'Clocked In', '2024-12-05 02:09:54', 'Clocked In - User ID: 69', '2024-12-05 02:09:54'),
(254, 66, 'Clocked In', '2024-12-05 02:26:33', 'Clocked In - User ID: 66', '2024-12-05 02:26:33'),
(255, 67, 'Clocked Out', '2024-12-05 02:34:08', 'Clocked Out - User ID: 67', '2024-12-05 02:34:08'),
(256, 74, 'Clocked In', '2024-12-05 02:34:37', 'Clocked In - User ID: 74', '2024-12-05 02:34:37'),
(257, 75, 'Clocked Out', '2024-12-05 02:34:39', 'Clocked Out - User ID: 75', '2024-12-05 02:34:39'),
(258, 68, 'Clocked In', '2024-12-05 02:34:43', 'Clocked In - User ID: 68', '2024-12-05 02:34:43'),
(259, 66, 'Login successful', '2024-12-05 02:41:21', 'Login successful - User ID: 66', '2024-12-05 02:41:21');

-- --------------------------------------------------------

--
-- Table structure for table `user_documents`
--

CREATE TABLE `user_documents` (
  `document_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `orcr` varchar(255) NOT NULL,
  `driverlicense` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_documents`
--

INSERT INTO `user_documents` (`document_id`, `user_id`, `orcr`, `driverlicense`) VALUES
(3, 66, '8f427928.jpg', 'dea02149.jpg'),
(4, 67, 'a5393991.jpg', '1bd57558.jpg'),
(5, 68, '6bb799be.jpg', 'b4dd170e.jpg'),
(6, 69, '6dcbe918.jpg', 'ac8ed471.jpg'),
(7, 70, 'f7310e81.jpg', 'e9de1b1d.jpg'),
(8, 71, '787b91d8.jpg', '2d7ca1ba.jpg'),
(9, 72, '3d2d0cff.jpg', '95181e45.jpg'),
(10, 74, '85340f01.jpg', '913e365e.jpg'),
(11, 75, 'b2edf96a.jpg', '9b699905.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `vehicle`
--

CREATE TABLE `vehicle` (
  `vehicle_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `licenseplate` varchar(255) NOT NULL,
  `make` varchar(255) NOT NULL,
  `model` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `rfid_no` varchar(255) NOT NULL,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicle`
--

INSERT INTO `vehicle` (`vehicle_id`, `user_id`, `licenseplate`, `make`, `model`, `created_at`, `rfid_no`, `deleted_at`) VALUES
(107, 66, 'CAX 3200', 'Ferrari', 'F12berlinetta', '2024-12-03 00:36:54', '0010605475', NULL),
(108, 67, 'CCA 2942', 'Chevrolet', 'Astro Passenger', '2024-12-04 23:05:51', '0004250133', NULL),
(109, 68, 'CAX 3295', 'Chevrolet', '3500 Regular Cab', '2024-12-04 23:08:32', '0004669639', NULL),
(110, 69, 'BAX 3129', 'Ford', 'Mustang', '2024-12-04 23:10:13', '0004290568', NULL),
(111, 70, 'CAB 9284', 'Ferrari', 'Roma', '2024-12-04 23:12:21', '0005398438', NULL),
(112, 71, 'GBU 2903', 'Toyota', 'Corolla', '2024-12-04 23:13:43', '0010571220', NULL),
(113, 72, 'CAB 9328', 'Fisker', 'Karma', '2024-12-04 23:14:49', '0010559824', NULL),
(115, 74, 'CAX 3294', 'Ford', 'E150 Super Duty Cargo', '2024-12-04 23:18:24', '0004724929', NULL),
(116, 75, 'CCA 9328', 'Jeep', 'Wrangler', '2024-12-04 23:20:39', '0011238051', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`),
  ADD KEY `fk_admin_password` (`password_id`);

--
-- Indexes for table `admin_activity_log`
--
ALTER TABLE `admin_activity_log`
  ADD PRIMARY KEY (`activity_id`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indexes for table `passwords`
--
ALTER TABLE `passwords`
  ADD PRIMARY KEY (`password_id`);

--
-- Indexes for table `rfid`
--
ALTER TABLE `rfid`
  ADD PRIMARY KEY (`rfid_id`),
  ADD KEY `rfid_no` (`rfid_no`);

--
-- Indexes for table `time_logs`
--
ALTER TABLE `time_logs`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `vehicle_id` (`vehicle_id`),
  ADD KEY `rfid_id` (`rfid_id`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `emp_no` (`emp_no`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `fk_user_password` (`password_id`);

--
-- Indexes for table `user_activity_log`
--
ALTER TABLE `user_activity_log`
  ADD PRIMARY KEY (`activity_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user_documents`
--
ALTER TABLE `user_documents`
  ADD PRIMARY KEY (`document_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `vehicle`
--
ALTER TABLE `vehicle`
  ADD PRIMARY KEY (`vehicle_id`),
  ADD UNIQUE KEY `licenseplate` (`licenseplate`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `fk_vehicle_rfid_no` (`rfid_no`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `admin_activity_log`
--
ALTER TABLE `admin_activity_log`
  MODIFY `activity_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=217;

--
-- AUTO_INCREMENT for table `passwords`
--
ALTER TABLE `passwords`
  MODIFY `password_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `rfid`
--
ALTER TABLE `rfid`
  MODIFY `rfid_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=127;

--
-- AUTO_INCREMENT for table `time_logs`
--
ALTER TABLE `time_logs`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=102;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=76;

--
-- AUTO_INCREMENT for table `user_activity_log`
--
ALTER TABLE `user_activity_log`
  MODIFY `activity_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=260;

--
-- AUTO_INCREMENT for table `user_documents`
--
ALTER TABLE `user_documents`
  MODIFY `document_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `vehicle`
--
ALTER TABLE `vehicle`
  MODIFY `vehicle_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=117;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admin`
--
ALTER TABLE `admin`
  ADD CONSTRAINT `fk_admin_password` FOREIGN KEY (`password_id`) REFERENCES `passwords` (`password_id`);

--
-- Constraints for table `admin_activity_log`
--
ALTER TABLE `admin_activity_log`
  ADD CONSTRAINT `admin_activity_log_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`) ON DELETE CASCADE;

--
-- Constraints for table `time_logs`
--
ALTER TABLE `time_logs`
  ADD CONSTRAINT `time_logs_ibfk_1` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle` (`vehicle_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `time_logs_ibfk_2` FOREIGN KEY (`rfid_id`) REFERENCES `rfid` (`rfid_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `time_logs_ibfk_3` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`);

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `fk_user_password` FOREIGN KEY (`password_id`) REFERENCES `passwords` (`password_id`);

--
-- Constraints for table `user_activity_log`
--
ALTER TABLE `user_activity_log`
  ADD CONSTRAINT `user_activity_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `user_documents`
--
ALTER TABLE `user_documents`
  ADD CONSTRAINT `user_documents_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

--
-- Constraints for table `vehicle`
--
ALTER TABLE `vehicle`
  ADD CONSTRAINT `fk_vehicle_rfid_no` FOREIGN KEY (`rfid_no`) REFERENCES `rfid` (`rfid_no`),
  ADD CONSTRAINT `fk_vehicle_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  ADD CONSTRAINT `vehicle_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
