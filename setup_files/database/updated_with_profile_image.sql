-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 13, 2024 at 01:26 PM
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
  `employee_id` int(11) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `contactnumber` varchar(15) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `profile_image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `employee_id`, `lastname`, `firstname`, `contactnumber`, `email`, `password`, `created_at`, `profile_image`) VALUES
(3, 123, 'Pelaez', 'Emanuel Luis', '09661970287', 'herroin29@gmail.com', 'scrypt:32768:8:1$Vlr9AVfJrC9ZUBpv$d00dedf419025258d40ae52c3aef5e96973730cf8b4ba703f75bbd49cd1094ef06848e5a606544be9713bd37304e13bec81cf8dffd465263451feba5e4f782a6', '2024-09-14 18:44:10', NULL),
(6, 0, 'Azarcon', 'John Francis', '09764274590', 'johnazarcon@gmail.com', 'scrypt:32768:8:1$oYV6AUbk546TGyTe$2f4429e500e4faa9e27f7f5679bd08a368d5856d10ffbe35c9ab952e05b85c35d5d26d77cbec58eb40c72afdd55708560b81ca5948ba4fffe8592b588d9f3e55', '2024-10-02 15:17:46', NULL);

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
(28, 3, 'Login successful', '2024-11-12 23:47:29', 'Login successful - User ID: 3', '2024-11-12 23:47:29'),
(29, 3, 'Login successful', '2024-11-13 00:23:47', 'Login successful - User ID: 3', '2024-11-13 00:23:47'),
(31, 3, 'Login successful', '2024-11-13 16:44:16', 'Login successful - User ID: 3', '2024-11-13 16:44:16'),
(32, 3, 'Login successful', '2024-11-13 16:56:28', 'Login successful - User ID: 3', '2024-11-13 16:56:28'),
(33, 3, 'Added new user', '2024-11-13 16:56:58', 'Added new user - User ID: 3', '2024-11-13 16:56:58'),
(34, 3, 'Login successful', '2024-11-13 18:18:29', 'Login successful - User ID: 3', '2024-11-13 18:18:29'),
(35, 3, 'Login successful', '2024-11-13 19:14:46', 'Login successful - User ID: 3', '2024-11-13 19:14:46'),
(36, 3, 'Login successful', '2024-11-13 19:23:41', 'Login successful - User ID: 3', '2024-11-13 19:23:41'),
(37, 3, 'Added vehicle and RFID to User ID 47', '2024-11-13 19:24:59', 'Added vehicle and RFID to User ID 47 - User ID: 3', '2024-11-13 19:24:59'),
(38, 3, 'Added new user', '2024-11-13 19:31:20', 'Added new user - User ID: 3', '2024-11-13 19:31:20'),
(39, 3, 'Login successful', '2024-11-13 19:59:37', 'Login successful - User ID: 3', '2024-11-13 19:59:37');

-- --------------------------------------------------------

--
-- Table structure for table `rfid`
--

CREATE TABLE `rfid` (
  `rfid_id` int(11) NOT NULL,
  `rfid_no` varchar(255) NOT NULL,
  `vehicle_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rfid`
--

INSERT INTO `rfid` (`rfid_id`, `rfid_no`, `vehicle_id`, `created_at`) VALUES
(86, '0004261965', 87, '2024-09-22 01:43:14'),
(88, '0010559824', 88, '2024-09-22 01:43:19'),
(89, '0010605475', 84, '2024-09-22 01:43:21'),
(90, '0010571220', 90, '2024-09-22 01:43:23'),
(91, '0004669639', 89, '2024-09-22 01:43:26'),
(92, '0011238051', 86, '2024-09-22 01:43:28'),
(93, '0005398438', 85, '2024-09-22 01:43:29'),
(96, '0004724929', NULL, '2024-09-23 01:52:41'),
(97, '0004250133', NULL, '2024-09-23 01:52:44'),
(98, '0004290568', NULL, '2024-09-23 01:52:47');

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
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `time_logs`
--

INSERT INTO `time_logs` (`log_id`, `vehicle_id`, `rfid_id`, `time_in`, `time_out`, `created_at`) VALUES
(9, 87, 86, '2024-09-23 02:53:12', '2024-09-23 02:53:38', '2024-09-23 02:53:12'),
(10, 88, 88, '2024-09-23 02:53:15', '2024-09-23 02:53:44', '2024-09-23 02:53:15'),
(11, 89, 91, '2024-09-23 02:53:18', '2024-09-23 02:53:46', '2024-09-23 02:53:18'),
(12, 90, 90, '2024-09-23 02:53:21', '2024-09-23 02:53:49', '2024-09-23 02:53:21'),
(13, 86, 92, '2024-09-23 02:53:24', '2024-09-23 02:53:51', '2024-09-23 02:53:24'),
(14, 84, 89, '2024-09-23 02:53:28', '2024-09-23 02:53:54', '2024-09-23 02:53:28'),
(15, 85, 93, '2024-09-23 02:53:32', '2024-09-23 02:53:56', '2024-09-23 02:53:32'),
(16, 87, 86, '2024-10-02 15:28:36', '2024-10-02 15:29:43', '2024-10-02 15:28:36'),
(17, 90, 90, '2024-10-02 15:30:49', '2024-10-02 15:31:08', '2024-10-02 15:30:49'),
(18, 89, 91, '2024-10-02 15:30:52', '2024-10-02 15:31:11', '2024-10-02 15:30:52'),
(19, 85, 93, '2024-10-02 15:30:54', '2024-10-02 15:31:15', '2024-10-02 15:30:54'),
(20, 84, 89, '2024-10-02 15:30:57', '2024-10-02 15:31:17', '2024-10-02 15:30:57');

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
  `password` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `profile_image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `emp_no`, `lastname`, `firstname`, `email`, `contactnumber`, `password`, `created_at`, `profile_image`) VALUES
(28, 'SUM2021-00366', 'Pelaez', 'Emanuel Luis', 'e.luis.pelaez@gmail.com', '09661970287', 'scrypt:32768:8:1$VRpws9r4l4fV2jyh$e58ec91f5368668e98430baa72099a648476fbef539a5e6ed6793eb5847b15009b5630f8b0b720af5e55e357c896a05f4740f2e91d4e141bcc8b7392b1b534f3', '2024-09-16 18:42:01', NULL),
(29, 'GTC2021-00232', 'Abrera', 'Juliecca', 'julieccaabrera@gmail.com', '09764829258', 'scrypt:32768:8:1$Nuz49hxARNlKbbG1$7a99f563f406b5dac5b02d6df03f53cff7a297cb732a42432a67d77ab5604f8f4a44a527fee2919e03cfc3dfe4f7317fc359a98f22dc653ba0ec6bc0f8363110', '2024-09-16 18:43:46', NULL),
(30, 'SUM2020-00296', 'Romero', 'Vinz Albert', 'vinzzzz@gmail.com', '09661970287', 'scrypt:32768:8:1$dTivDKdgdIXc2eTk$2337f1d9abbea4a90b305fe7a794fcf184f915b921744faa168f8e6c874c07160e8a15b41c392217e1fc3ead857cb4304c8a5f20a2d4b5268ac39b9d07b12dd0', '2024-09-16 18:45:06', NULL),
(31, 'SUM2020-00284', 'Facundo', 'Ford', 'fooorrddddd@gmail.com', '09752837485', 'scrypt:32768:8:1$oYCmNxudcenM1RiY$a06b1c9f4320d668134bc97a5deb4129bb94f5546b5b2fae7c9eeade2618bdedae23f81d16de6c5249134be1f840e4f6dc46e9cb0cde54ba735ba0802481e38a', '2024-09-16 18:47:33', NULL),
(32, 'SLU-GB-007', 'Laygo', 'Ro-eh Israel', 'roooeeeehhhhh@gmail.com', '09752837485', 'scrypt:32768:8:1$6IjftieF04MuXSAu$c0453dc8db3d18534636f8516fc00cb9cec904cbff28f334842ba84804762656093f60bf9a6a801d2de3e32ec360a6d9333ed33002939d3988e07355612687a0', '2024-09-16 18:48:39', NULL),
(33, 'SLU-GB-008', 'Angelo', 'Shem', 'sheeeeemmm@gmail.com', '09661970287', 'scrypt:32768:8:1$o7cbPl6O25AoSPWj$916cca9c005597853a343944f96a88976c02d6e7ebd4233914f653dffaaf8522cf1ce084c258fc8a3d46696cf18f13fcab9237c0ea48eb6715fa5229c081cdbd', '2024-09-16 18:50:06', NULL),
(35, 'SUM2020-00281', 'Manapol', 'Patrick Mel', 'patriccckkk@gmail.com', '09752832345', 'scrypt:32768:8:1$ouGLrjWVMpZovqep$c8e3ff1d36521a4377a2307ff4b075b03c308f359c82666852e1d405cf4dae9ddc3a50c5f8296a66c95f34bcd54c76afb39a3ff0c5ce0503ef81196997d2aed6', '2024-09-16 18:51:18', NULL),
(36, 'WUP-CC-069', 'Puyat', 'Yuri', 'yuriiiiiii@gmail.com', '09764274738', 'scrypt:32768:8:1$a1UelWpvxmq37kxY$a72f1eb203710349946d2acff7417bb5ffe964dfd49ee8ae5b0d5ec633375533a56427c48817cc2456c292ded024c0994746ee9ed31aeb6d3fccab2dddefd9d7', '2024-09-16 18:52:25', NULL),
(37, 'GTC2020-00690', 'Ferry', 'Ryz', 'ryyyyzzz@gmail.com', '09661972948', 'scrypt:32768:8:1$S3FXJ9dKedZsxTom$fcb28360cf32907379750dd3a53179c9544285d43ad15d2b669b2dbce945d72fa774ab674ac49a31d7b6c054e90ca08260676b40f816b95a047500159b67ef49', '2024-09-16 18:52:59', NULL),
(38, 'CLSU-0069', 'Grospe', 'Ellmar', 'elllmaaaarrrr@gmail.com', '09752845782', 'scrypt:32768:8:1$5Jco7kbeQjG7HOh3$766cae1bceb624e6fb1e98343fe407d84edc2be70d1afa31cbb4b671288e1402d0061e52432e01a932e9e43e40bc3aa422d375a081bf411d9257dd6fb5dd1274', '2024-09-16 18:53:55', NULL),
(39, 'SUM2020-002650', 'Cucio', 'Julian CARLOS', 'juliiiaaaannn@gmail.com', '09661972373', 'scrypt:32768:8:1$UuTqWUGgSjnWeoXC$0c77ba035f0ce5b4ac788efcf7621d407fed2994100374cb1e7e2ca3601716437c2844a85aff49d8fd5e5fa46132e1565dc619f8b67b66e61ce3b24862b5fdfa', '2024-09-16 18:57:09', NULL);

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
(69, 28, 'Login Successful', '2024-10-09 19:50:53', 'Login Successful - User ID: 28', '2024-10-09 19:50:53'),
(75, 28, 'Login Successful', '2024-11-13 19:40:23', 'Login Successful - User ID: 28', '2024-11-13 19:40:23'),
(76, 28, 'Login Successful', '2024-11-13 19:47:49', 'Login Successful - User ID: 28', '2024-11-13 19:47:49'),
(77, 28, 'Login Successful', '2024-11-13 19:49:17', 'Login Successful - User ID: 28', '2024-11-13 19:49:17'),
(78, 28, 'Login Successful', '2024-11-13 19:52:37', 'Login Successful - User ID: 28', '2024-11-13 19:52:37'),
(79, 28, 'Login Successful', '2024-11-13 19:55:24', 'Login Successful - User ID: 28', '2024-11-13 19:55:24');

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
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicle`
--

INSERT INTO `vehicle` (`vehicle_id`, `user_id`, `licenseplate`, `make`, `model`, `created_at`) VALUES
(84, 28, 'SUM 2934', 'Cadillac', 'CTS', '2024-09-23 01:46:34'),
(85, 38, 'COR 2934', 'Bentley', 'Mulsanne', '2024-09-23 01:47:21'),
(86, 37, 'DJW 2394', 'Ford', 'Focus', '2024-09-23 01:47:45'),
(87, 33, 'SHE 2456', 'Suzuki', 'Swift', '2024-09-23 01:48:13'),
(88, 28, 'CCA 2945', 'BMW', 'X6 M', '2024-09-23 01:48:42'),
(89, 29, 'CCA 2946', 'Jeep', 'Patriot', '2024-09-23 01:49:04'),
(90, 32, 'ROE 2945', 'Ferrari', 'California', '2024-09-23 01:49:24');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `admin_activity_log`
--
ALTER TABLE `admin_activity_log`
  ADD PRIMARY KEY (`activity_id`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indexes for table `rfid`
--
ALTER TABLE `rfid`
  ADD PRIMARY KEY (`rfid_id`),
  ADD UNIQUE KEY `rfid_no` (`rfid_no`),
  ADD UNIQUE KEY `vehicle_id` (`vehicle_id`);

--
-- Indexes for table `time_logs`
--
ALTER TABLE `time_logs`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `vehicle_id` (`vehicle_id`),
  ADD KEY `rfid_id` (`rfid_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `emp_no` (`emp_no`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `user_activity_log`
--
ALTER TABLE `user_activity_log`
  ADD PRIMARY KEY (`activity_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `vehicle`
--
ALTER TABLE `vehicle`
  ADD PRIMARY KEY (`vehicle_id`),
  ADD UNIQUE KEY `licenseplate` (`licenseplate`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `admin_activity_log`
--
ALTER TABLE `admin_activity_log`
  MODIFY `activity_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `rfid`
--
ALTER TABLE `rfid`
  MODIFY `rfid_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=99;

--
-- AUTO_INCREMENT for table `time_logs`
--
ALTER TABLE `time_logs`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `user_activity_log`
--
ALTER TABLE `user_activity_log`
  MODIFY `activity_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=80;

--
-- AUTO_INCREMENT for table `vehicle`
--
ALTER TABLE `vehicle`
  MODIFY `vehicle_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=94;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admin_activity_log`
--
ALTER TABLE `admin_activity_log`
  ADD CONSTRAINT `admin_activity_log_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`) ON DELETE CASCADE;

--
-- Constraints for table `rfid`
--
ALTER TABLE `rfid`
  ADD CONSTRAINT `rfid_ibfk_1` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle` (`vehicle_id`) ON DELETE SET NULL;

--
-- Constraints for table `time_logs`
--
ALTER TABLE `time_logs`
  ADD CONSTRAINT `time_logs_ibfk_1` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle` (`vehicle_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `time_logs_ibfk_2` FOREIGN KEY (`rfid_id`) REFERENCES `rfid` (`rfid_id`) ON DELETE CASCADE;

--
-- Constraints for table `user_activity_log`
--
ALTER TABLE `user_activity_log`
  ADD CONSTRAINT `user_activity_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `vehicle`
--
ALTER TABLE `vehicle`
  ADD CONSTRAINT `vehicle_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
