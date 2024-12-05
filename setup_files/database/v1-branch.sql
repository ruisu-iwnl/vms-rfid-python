-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 28, 2024 at 02:03 PM
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
  `password` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `profile_image` varchar(255) DEFAULT NULL,
  `is_super_admin` tinyint(1) DEFAULT 0,
  `deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `employee_id`, `lastname`, `firstname`, `contactnumber`, `email`, `password`, `created_at`, `profile_image`, `is_super_admin`, `deleted_at`) VALUES
(3, 'SUM2021-00366', 'Pelaez', 'Emanuel Luis', '09661970287', 'e.luis.pelaez@gmail.com', 'scrypt:32768:8:1$Vlr9AVfJrC9ZUBpv$d00dedf419025258d40ae52c3aef5e96973730cf8b4ba703f75bbd49cd1094ef06848e5a606544be9713bd37304e13bec81cf8dffd465263451feba5e4f782a6', '2024-09-14 18:44:10', '2x2.png', 1, NULL),
(6, 'SUM2021-01544', 'Azarcon', 'John Francis', '09764274590', 'johnazarcon@gmail.com', 'scrypt:32768:8:1$oYV6AUbk546TGyTe$2f4429e500e4faa9e27f7f5679bd08a368d5856d10ffbe35c9ab952e05b85c35d5d26d77cbec58eb40c72afdd55708560b81ca5948ba4fffe8592b588d9f3e55', '2024-10-02 15:17:46', 'jj.png', 0, NULL),
(13, 'SUM2021-00492', 'Naagas', 'Jazper', '09784724656', 'jazpertom@gmail.com', 'scrypt:32768:8:1$lpaLyG1wMyY3erl5$5e7fcb161e718ba47ff80013edf0b78dd91573c561b44bda51f4d651cd25e3f3ca046312b12e349007a9260042a47167d2808585cfe3b888af8556bab4c1628b', '2024-11-16 23:11:32', 'jazper.png', 1, '2024-11-16 15:23:56'),
(14, 'SUM292931', 'Wrestling', 'Johnny', '09784274592', 'johnnywrestling@gmail.com', 'scrypt:32768:8:1$qKlteToiTV9Q0zLV$8889c5bc7e1c035cc8e0f4b1152139402e82125f501795a19742b627bd589442b9095cd0f6dd97d325fe129fb6c20d17b4cede72021d7bb7d585eedb6cc039cd', '2024-11-19 02:12:27', 'vinz.jpg', 0, NULL);

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
(54, 3, 'Login successful', '2024-11-15 01:47:05', 'Login successful - User ID: 3', '2024-11-15 01:47:05'),
(55, 3, 'Login successful', '2024-11-15 02:14:22', 'Login successful - User ID: 3', '2024-11-15 02:14:22'),
(56, 3, 'Login successful', '2024-11-15 02:18:15', 'Login successful - User ID: 3', '2024-11-15 02:18:15'),
(57, 3, 'Login successful', '2024-11-15 02:23:54', 'Login successful - User ID: 3', '2024-11-15 02:23:54'),
(58, 3, 'Login successful', '2024-11-15 02:36:20', 'Login successful - User ID: 3', '2024-11-15 02:36:20'),
(59, 3, 'Added new user', '2024-11-15 03:05:49', 'Added new user - User ID: 3', '2024-11-15 03:05:49'),
(60, 3, 'Login successful', '2024-11-15 18:06:52', 'Login successful - User ID: 3', '2024-11-15 18:06:52'),
(61, 3, 'Login successful', '2024-11-15 19:12:32', 'Login successful - User ID: 3', '2024-11-15 19:12:32'),
(62, 3, 'Login successful', '2024-11-15 19:15:28', 'Login successful - User ID: 3', '2024-11-15 19:15:28'),
(63, 3, 'Login successful', '2024-11-15 20:04:42', 'Login successful - User ID: 3', '2024-11-15 20:04:42'),
(65, 3, 'Login successful', '2024-11-15 20:26:11', 'Login successful - User ID: 3', '2024-11-15 20:26:11'),
(66, 3, 'Login successful', '2024-11-15 20:28:48', 'Login successful - User ID: 3', '2024-11-15 20:28:48'),
(67, 3, 'Login successful', '2024-11-15 20:30:02', 'Login successful - User ID: 3', '2024-11-15 20:30:02'),
(68, 3, 'Login successful', '2024-11-15 20:33:38', 'Login successful - User ID: 3', '2024-11-15 20:33:38'),
(69, 3, 'Login successful', '2024-11-15 20:41:52', 'Login successful - User ID: 3', '2024-11-15 20:41:52'),
(70, 3, 'Login successful', '2024-11-15 20:42:58', 'Login successful - User ID: 3', '2024-11-15 20:42:58'),
(71, 3, 'Login successful', '2024-11-15 20:45:48', 'Login successful - User ID: 3', '2024-11-15 20:45:48'),
(72, 3, 'Login successful', '2024-11-15 21:00:35', 'Login successful - User ID: 3', '2024-11-15 21:00:35'),
(73, 3, 'Login successful', '2024-11-15 21:06:11', 'Login successful - User ID: 3', '2024-11-15 21:06:11'),
(74, 3, 'Login successful', '2024-11-15 21:07:58', 'Login successful - User ID: 3', '2024-11-15 21:07:58'),
(75, 3, 'Login successful', '2024-11-15 21:09:57', 'Login successful - User ID: 3', '2024-11-15 21:09:57'),
(76, 3, 'Login successful', '2024-11-15 21:29:26', 'Login successful - User ID: 3', '2024-11-15 21:29:26'),
(77, 3, 'Added new admin', '2024-11-15 21:29:48', 'Added new admin - User ID: 3', '2024-11-15 21:29:48'),
(78, 3, 'Login successful', '2024-11-15 21:33:04', 'Login successful - User ID: 3', '2024-11-15 21:33:04'),
(79, 3, 'Login successful', '2024-11-15 21:50:34', 'Login successful - User ID: 3', '2024-11-15 21:50:34'),
(80, 3, 'Login successful', '2024-11-15 21:51:45', 'Login successful - User ID: 3', '2024-11-15 21:51:45'),
(81, 3, 'Added new admin', '2024-11-15 21:57:12', 'Added new admin - User ID: 3', '2024-11-15 21:57:12'),
(82, 3, 'Login successful', '2024-11-15 23:28:13', 'Login successful - User ID: 3', '2024-11-15 23:28:13'),
(83, 3, 'Login successful', '2024-11-15 23:30:04', 'Login successful - User ID: 3', '2024-11-15 23:30:04'),
(84, 3, 'Login successful', '2024-11-16 00:29:57', 'Login successful - User ID: 3', '2024-11-16 00:29:57'),
(85, 3, 'Login successful', '2024-11-16 14:49:41', 'Login successful - User ID: 3', '2024-11-16 14:49:41'),
(86, 3, 'Login successful', '2024-11-16 14:51:36', 'Login successful - User ID: 3', '2024-11-16 14:51:36'),
(87, 3, 'Login successful', '2024-11-16 14:57:06', 'Login successful - User ID: 3', '2024-11-16 14:57:06'),
(88, 3, 'Login successful', '2024-11-16 15:12:59', 'Login successful - User ID: 3', '2024-11-16 15:12:59'),
(89, 3, 'Login successful', '2024-11-16 16:20:29', 'Login successful - User ID: 3', '2024-11-16 16:20:29'),
(90, 3, 'Login successful', '2024-11-16 17:35:32', 'Login successful - User ID: 3', '2024-11-16 17:35:32'),
(91, 3, 'Login successful', '2024-11-16 18:24:50', 'Login successful - User ID: 3', '2024-11-16 18:24:50'),
(92, 3, 'Login successful', '2024-11-16 18:29:39', 'Login successful - User ID: 3', '2024-11-16 18:29:39'),
(93, 3, 'Login successful', '2024-11-16 18:45:52', 'Login successful - User ID: 3', '2024-11-16 18:45:52'),
(94, 3, 'Login successful', '2024-11-16 18:58:37', 'Login successful - User ID: 3', '2024-11-16 18:58:37'),
(95, 3, 'Login successful', '2024-11-16 19:00:35', 'Login successful - User ID: 3', '2024-11-16 19:00:35'),
(96, 3, 'Login successful', '2024-11-16 19:27:09', 'Login successful - User ID: 3', '2024-11-16 19:27:09'),
(97, 3, 'Login successful', '2024-11-16 19:35:27', 'Login successful - User ID: 3', '2024-11-16 19:35:27'),
(98, 3, 'Login successful', '2024-11-16 19:44:20', 'Login successful - User ID: 3', '2024-11-16 19:44:20'),
(99, 3, 'Login successful', '2024-11-16 19:53:12', 'Login successful - User ID: 3', '2024-11-16 19:53:12'),
(100, 3, 'Login successful', '2024-11-16 19:56:23', 'Login successful - User ID: 3', '2024-11-16 19:56:23'),
(101, 3, 'Login successful', '2024-11-16 19:58:06', 'Login successful - User ID: 3', '2024-11-16 19:58:06'),
(102, 3, 'Login successful', '2024-11-16 20:01:38', 'Login successful - User ID: 3', '2024-11-16 20:01:38'),
(103, 3, 'Login successful', '2024-11-16 20:06:05', 'Login successful - User ID: 3', '2024-11-16 20:06:05'),
(104, 3, 'Login successful', '2024-11-16 20:09:19', 'Login successful - User ID: 3', '2024-11-16 20:09:19'),
(105, 3, 'Login successful', '2024-11-16 20:21:56', 'Login successful - User ID: 3', '2024-11-16 20:21:56'),
(106, 3, 'Added vehicle and RFID to User ID 39', '2024-11-16 20:38:19', 'Added vehicle and RFID to User ID 39 - User ID: 3', '2024-11-16 20:38:19'),
(107, 3, 'Login successful', '2024-11-16 20:40:47', 'Login successful - User ID: 3', '2024-11-16 20:40:47'),
(108, 3, 'Login successful', '2024-11-16 20:57:53', 'Login successful - User ID: 3', '2024-11-16 20:57:53'),
(109, 3, 'Login successful', '2024-11-16 21:12:14', 'Login successful - User ID: 3', '2024-11-16 21:12:14'),
(110, 3, 'Login successful', '2024-11-16 21:19:22', 'Login successful - User ID: 3', '2024-11-16 21:19:22'),
(111, 3, 'Login successful', '2024-11-16 21:27:54', 'Login successful - User ID: 3', '2024-11-16 21:27:54'),
(112, 3, 'Login successful', '2024-11-16 21:42:10', 'Login successful - User ID: 3', '2024-11-16 21:42:10'),
(113, 3, 'Login successful', '2024-11-16 21:48:09', 'Login successful - User ID: 3', '2024-11-16 21:48:09'),
(114, 3, 'Login successful', '2024-11-16 21:53:09', 'Login successful - User ID: 3', '2024-11-16 21:53:09'),
(115, 3, 'Login successful', '2024-11-16 21:56:35', 'Login successful - User ID: 3', '2024-11-16 21:56:35'),
(116, 3, 'Login successful', '2024-11-16 22:04:27', 'Login successful - User ID: 3', '2024-11-16 22:04:27'),
(117, 3, 'Login successful', '2024-11-16 22:06:58', 'Login successful - User ID: 3', '2024-11-16 22:06:58'),
(118, 3, 'Login successful', '2024-11-16 22:09:05', 'Login successful - User ID: 3', '2024-11-16 22:09:05'),
(119, 3, 'Login successful', '2024-11-16 22:10:37', 'Login successful - User ID: 3', '2024-11-16 22:10:37'),
(120, 3, 'Login successful', '2024-11-16 22:12:50', 'Login successful - User ID: 3', '2024-11-16 22:12:50'),
(121, 3, 'Login successful', '2024-11-16 22:19:16', 'Login successful - User ID: 3', '2024-11-16 22:19:16'),
(122, 3, 'Login successful', '2024-11-16 22:21:24', 'Login successful - User ID: 3', '2024-11-16 22:21:24'),
(123, 3, 'Login successful', '2024-11-16 22:22:27', 'Login successful - User ID: 3', '2024-11-16 22:22:27'),
(124, 3, 'Login successful', '2024-11-16 22:24:54', 'Login successful - User ID: 3', '2024-11-16 22:24:54'),
(125, 3, 'Login successful', '2024-11-16 22:30:33', 'Login successful - User ID: 3', '2024-11-16 22:30:33'),
(126, 3, 'Login successful', '2024-11-16 22:32:22', 'Login successful - User ID: 3', '2024-11-16 22:32:22'),
(127, 3, 'Login successful', '2024-11-16 22:34:32', 'Login successful - User ID: 3', '2024-11-16 22:34:32'),
(128, 3, 'Login successful', '2024-11-16 22:37:01', 'Login successful - User ID: 3', '2024-11-16 22:37:01'),
(129, 3, 'Login successful', '2024-11-16 22:39:46', 'Login successful - User ID: 3', '2024-11-16 22:39:46'),
(130, 3, 'Login successful', '2024-11-16 22:53:11', 'Login successful - User ID: 3', '2024-11-16 22:53:11'),
(131, 3, 'Toggled Super Admin Status for admin 6', '2024-11-16 22:56:37', 'Toggled Super Admin Status for admin 6 - User ID: 3', '2024-11-16 22:56:37'),
(132, 3, 'Toggled Super Admin Status for admin 6', '2024-11-16 22:56:41', 'Toggled Super Admin Status for admin 6 - User ID: 3', '2024-11-16 22:56:41'),
(133, 3, 'Toggled Super Admin Status for admin 6', '2024-11-16 22:56:45', 'Toggled Super Admin Status for admin 6 - User ID: 3', '2024-11-16 22:56:45'),
(134, 3, 'Toggled Super Admin Status for admin 6', '2024-11-16 22:56:54', 'Toggled Super Admin Status for admin 6 - User ID: 3', '2024-11-16 22:56:54'),
(135, 3, 'Toggled Super Admin Status for admin 6', '2024-11-16 22:57:05', 'Toggled Super Admin Status for admin 6 - User ID: 3', '2024-11-16 22:57:05'),
(136, 3, 'Login successful', '2024-11-16 23:00:52', 'Login successful - User ID: 3', '2024-11-16 23:00:52'),
(137, 3, 'Toggled Super Admin Status for admin 6', '2024-11-16 23:00:56', 'Toggled Super Admin Status for admin 6 - User ID: 3', '2024-11-16 23:00:56'),
(138, 3, 'Toggled Super Admin Status for admin 6', '2024-11-16 23:01:07', 'Toggled Super Admin Status for admin 6 - User ID: 3', '2024-11-16 23:01:07'),
(139, 3, 'Toggled Super Admin Status for admin 6', '2024-11-16 23:01:11', 'Toggled Super Admin Status for admin 6 - User ID: 3', '2024-11-16 23:01:11'),
(140, 3, 'Toggled Super Admin Status for admin 6', '2024-11-16 23:03:20', 'Toggled Super Admin Status for admin 6 - User ID: 3', '2024-11-16 23:03:20'),
(141, 3, 'Toggled Super Admin Status for admin 6', '2024-11-16 23:03:25', 'Toggled Super Admin Status for admin 6 - User ID: 3', '2024-11-16 23:03:25'),
(142, 3, 'Login successful', '2024-11-16 23:08:18', 'Login successful - User ID: 3', '2024-11-16 23:08:18'),
(143, 3, 'Added new admin', '2024-11-16 23:11:32', 'Added new admin - User ID: 3', '2024-11-16 23:11:32'),
(144, 13, 'Login successful', '2024-11-16 23:11:57', 'Login successful - User ID: 13', '2024-11-16 23:11:57'),
(145, 3, 'Login successful', '2024-11-16 23:13:27', 'Login successful - User ID: 3', '2024-11-16 23:13:27'),
(146, 3, 'Toggled Super Admin Status for admin 13', '2024-11-16 23:13:37', 'Toggled Super Admin Status for admin 13 - User ID: 3', '2024-11-16 23:13:37'),
(147, 13, 'Login successful', '2024-11-16 23:14:02', 'Login successful - User ID: 13', '2024-11-16 23:14:02'),
(148, 3, 'Login successful', '2024-11-16 23:15:14', 'Login successful - User ID: 3', '2024-11-16 23:15:14'),
(149, 3, 'Login successful', '2024-11-16 23:17:56', 'Login successful - User ID: 3', '2024-11-16 23:17:56'),
(150, 13, 'Login successful', '2024-11-16 23:18:50', 'Login successful - User ID: 13', '2024-11-16 23:18:50'),
(151, 13, 'Login successful', '2024-11-16 23:23:26', 'Login successful - User ID: 13', '2024-11-16 23:23:26'),
(152, 3, 'Login successful', '2024-11-16 23:23:51', 'Login successful - User ID: 3', '2024-11-16 23:23:51'),
(153, 3, 'Soft-deleted admin 13', '2024-11-16 23:23:56', 'Soft-deleted admin 13 - User ID: 3', '2024-11-16 23:23:56'),
(154, 3, 'Login successful', '2024-11-17 00:00:32', 'Login successful - User ID: 3', '2024-11-17 00:00:32'),
(155, 3, 'Login successful', '2024-11-17 17:55:08', 'Login successful - User ID: 3', '2024-11-17 17:55:08'),
(156, 3, 'Toggled Super Admin Status for admin 6', '2024-11-17 17:55:39', 'Toggled Super Admin Status for admin 6 - User ID: 3', '2024-11-17 17:55:39'),
(157, 3, 'Login successful', '2024-11-18 21:21:33', 'Login successful - User ID: 3', '2024-11-18 21:21:33'),
(158, 3, 'Login successful', '2024-11-18 21:43:26', 'Login successful - User ID: 3', '2024-11-18 21:43:26'),
(159, 3, 'Login successful', '2024-11-18 21:44:52', 'Login successful - User ID: 3', '2024-11-18 21:44:52'),
(160, 3, 'Login successful', '2024-11-18 22:04:06', 'Login successful - User ID: 3', '2024-11-18 22:04:06'),
(161, 3, 'Login successful', '2024-11-18 22:06:34', 'Login successful - User ID: 3', '2024-11-18 22:06:34'),
(162, 3, 'Login successful', '2024-11-18 22:08:00', 'Login successful - User ID: 3', '2024-11-18 22:08:00'),
(163, 3, 'Login successful', '2024-11-18 22:09:13', 'Login successful - User ID: 3', '2024-11-18 22:09:13'),
(164, 3, 'Login successful', '2024-11-18 22:10:43', 'Login successful - User ID: 3', '2024-11-18 22:10:43'),
(165, 3, 'Login successful', '2024-11-18 22:12:24', 'Login successful - User ID: 3', '2024-11-18 22:12:24'),
(166, 3, 'Login successful', '2024-11-18 22:15:25', 'Login successful - User ID: 3', '2024-11-18 22:15:25'),
(167, 3, 'Login successful', '2024-11-18 22:16:44', 'Login successful - User ID: 3', '2024-11-18 22:16:44'),
(168, 3, 'Login successful', '2024-11-18 22:18:53', 'Login successful - User ID: 3', '2024-11-18 22:18:53'),
(169, 3, 'Login successful', '2024-11-18 22:20:15', 'Login successful - User ID: 3', '2024-11-18 22:20:15'),
(170, 3, 'Login successful', '2024-11-18 22:20:19', 'Login successful - User ID: 3', '2024-11-18 22:20:19'),
(171, 3, 'Login successful', '2024-11-18 22:22:20', 'Login successful - User ID: 3', '2024-11-18 22:22:20'),
(172, 3, 'Login successful', '2024-11-18 22:25:04', 'Login successful - User ID: 3', '2024-11-18 22:25:04'),
(173, 3, 'Login successful', '2024-11-18 22:27:10', 'Login successful - User ID: 3', '2024-11-18 22:27:10'),
(174, 3, 'Login successful', '2024-11-18 22:28:45', 'Login successful - User ID: 3', '2024-11-18 22:28:45'),
(175, 3, 'Login successful', '2024-11-18 22:30:59', 'Login successful - User ID: 3', '2024-11-18 22:30:59'),
(176, 3, 'Login successful', '2024-11-18 22:31:03', 'Login successful - User ID: 3', '2024-11-18 22:31:03'),
(177, 3, 'Login successful', '2024-11-18 22:33:02', 'Login successful - User ID: 3', '2024-11-18 22:33:02'),
(178, 3, 'Login successful', '2024-11-18 22:33:19', 'Login successful - User ID: 3', '2024-11-18 22:33:19'),
(179, 3, 'Login successful', '2024-11-18 22:35:13', 'Login successful - User ID: 3', '2024-11-18 22:35:13'),
(180, 3, 'Login successful', '2024-11-18 22:38:08', 'Login successful - User ID: 3', '2024-11-18 22:38:08'),
(181, 3, 'Login successful', '2024-11-18 22:44:20', 'Login successful - User ID: 3', '2024-11-18 22:44:20'),
(182, 3, 'Login successful', '2024-11-18 22:47:51', 'Login successful - User ID: 3', '2024-11-18 22:47:51'),
(183, 3, 'Login successful', '2024-11-18 23:07:21', 'Login successful - User ID: 3', '2024-11-18 23:07:21'),
(184, 3, 'Login successful', '2024-11-18 23:37:56', 'Login successful - User ID: 3', '2024-11-18 23:37:56'),
(185, 3, 'Toggled Super Admin Status for admin 6', '2024-11-18 23:43:18', 'Toggled Super Admin Status for admin 6 - User ID: 3', '2024-11-18 23:43:18'),
(186, 3, 'Toggled Super Admin Status for admin 6', '2024-11-18 23:43:19', 'Toggled Super Admin Status for admin 6 - User ID: 3', '2024-11-18 23:43:19'),
(187, 3, 'Login successful', '2024-11-19 01:55:47', 'Login successful - User ID: 3', '2024-11-19 01:55:47'),
(188, 3, 'Login successful', '2024-11-19 02:02:27', 'Login successful - User ID: 3', '2024-11-19 02:02:27'),
(189, 3, 'Added new admin', '2024-11-19 02:12:27', 'Added new admin - User ID: 3', '2024-11-19 02:12:27'),
(190, 14, 'Login successful', '2024-11-19 02:12:57', 'Login successful - User ID: 14', '2024-11-19 02:12:57'),
(191, 3, 'Login successful', '2024-11-19 02:15:35', 'Login successful - User ID: 3', '2024-11-19 02:15:35'),
(192, 3, 'Login successful', '2024-11-23 14:16:40', 'Login successful - User ID: 3', '2024-11-23 14:16:40'),
(193, 3, 'Login successful', '2024-11-23 14:23:42', 'Login successful - User ID: 3', '2024-11-23 14:23:42'),
(194, 3, 'Login successful', '2024-11-23 14:27:23', 'Login successful - User ID: 3', '2024-11-23 14:27:23'),
(195, 3, 'Login successful', '2024-11-28 21:02:22', 'Login successful - User ID: 3', '2024-11-28 21:02:22'),
(196, 3, 'Toggled Super Admin Status for admin 6', '2024-11-28 21:03:05', 'Toggled Super Admin Status for admin 6 - User ID: 3', '2024-11-28 21:03:05'),
(197, 3, 'Toggled Super Admin Status for admin 6', '2024-11-28 21:03:06', 'Toggled Super Admin Status for admin 6 - User ID: 3', '2024-11-28 21:03:06');

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
(91, '0004669639', NULL, '2024-09-22 01:43:26'),
(92, '0011238051', 86, '2024-09-22 01:43:28'),
(93, '0005398438', 85, '2024-09-22 01:43:29'),
(96, '0004724929', NULL, '2024-09-23 01:52:41'),
(97, '0004250133', NULL, '2024-09-23 01:52:44'),
(98, '0004290568', 98, '2024-09-23 01:52:47');

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
(61, 90, 90, '2024-11-16 15:02:52', '2024-11-18 21:45:30', '2024-11-16 15:02:52'),
(62, 85, 93, '2024-11-16 15:03:07', '2024-11-18 21:45:26', '2024-11-16 15:03:07'),
(70, 84, 89, '2024-11-16 21:56:59', NULL, '2024-11-18 21:56:59'),
(80, 84, 89, '2024-11-18 23:42:18', '2024-11-19 01:56:12', '2024-11-18 23:42:18'),
(81, 84, 89, '2024-11-15 01:00:32', NULL, '2024-11-19 01:56:32'),
(82, 84, 89, '2024-11-19 02:04:49', NULL, '2024-11-19 02:04:49'),
(83, 84, 89, '2024-11-23 14:24:56', NULL, '2024-11-23 14:24:56');

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
(28, 'SUM2021-00366', 'Pelaez', 'Emanuel Luis', 'e.luispelaez@gmail.com', '09661970287', 'scrypt:32768:8:1$VRpws9r4l4fV2jyh$e58ec91f5368668e98430baa72099a648476fbef539a5e6ed6793eb5847b15009b5630f8b0b720af5e55e357c896a05f4740f2e91d4e141bcc8b7392b1b534f3', '2024-09-16 18:42:01', '2x2.png'),
(30, 'SUM2020-00296', 'Romero', 'Vinz Albert', 'vinzzzz@gmail.com', '09661970287', 'scrypt:32768:8:1$dTivDKdgdIXc2eTk$2337f1d9abbea4a90b305fe7a794fcf184f915b921744faa168f8e6c874c07160e8a15b41c392217e1fc3ead857cb4304c8a5f20a2d4b5268ac39b9d07b12dd0', '2024-09-16 18:45:06', 'vinz.jpg'),
(31, 'SUM2020-00284', 'Facundo', 'Ford', 'fooorrddddd@gmail.com', '09752837485', 'scrypt:32768:8:1$oYCmNxudcenM1RiY$a06b1c9f4320d668134bc97a5deb4129bb94f5546b5b2fae7c9eeade2618bdedae23f81d16de6c5249134be1f840e4f6dc46e9cb0cde54ba735ba0802481e38a', '2024-09-16 18:47:33', '2M.jpeg'),
(32, 'SLU-GB-007', 'Laygo', 'Ro-eh Israel', 'roooeeeehhhhh@gmail.com', '09752837485', 'scrypt:32768:8:1$6IjftieF04MuXSAu$c0453dc8db3d18534636f8516fc00cb9cec904cbff28f334842ba84804762656093f60bf9a6a801d2de3e32ec360a6d9333ed33002939d3988e07355612687a0', '2024-09-16 18:48:39', '3M.jpeg'),
(33, 'SLU-GB-008', 'Angelo', 'Shem', 'sheeeeemmm@gmail.com', '09661970287', 'scrypt:32768:8:1$o7cbPl6O25AoSPWj$916cca9c005597853a343944f96a88976c02d6e7ebd4233914f653dffaaf8522cf1ce084c258fc8a3d46696cf18f13fcab9237c0ea48eb6715fa5229c081cdbd', '2024-09-16 18:50:06', '4M.jpeg'),
(35, 'SUM2020-00281', 'Manapol', 'Patrick Mel', 'patriccckkk@gmail.com', '09752832345', 'scrypt:32768:8:1$ouGLrjWVMpZovqep$c8e3ff1d36521a4377a2307ff4b075b03c308f359c82666852e1d405cf4dae9ddc3a50c5f8296a66c95f34bcd54c76afb39a3ff0c5ce0503ef81196997d2aed6', '2024-09-16 18:51:18', '5M.jpeg'),
(36, 'WUP-CC-069', 'Puyat', 'Yuri', 'yuriiiiiii@gmail.com', '09764274738', 'scrypt:32768:8:1$a1UelWpvxmq37kxY$a72f1eb203710349946d2acff7417bb5ffe964dfd49ee8ae5b0d5ec633375533a56427c48817cc2456c292ded024c0994746ee9ed31aeb6d3fccab2dddefd9d7', '2024-09-16 18:52:25', '6M.jpeg'),
(37, 'GTC2020-00690', 'Ferry', 'Ryz', 'ryyyyzzz@gmail.com', '09661972948', 'scrypt:32768:8:1$S3FXJ9dKedZsxTom$fcb28360cf32907379750dd3a53179c9544285d43ad15d2b669b2dbce945d72fa774ab674ac49a31d7b6c054e90ca08260676b40f816b95a047500159b67ef49', '2024-09-16 18:52:59', '7M.jpeg'),
(38, 'CLSU-0069', 'Grospe', 'Ellmar', 'elllmaaaarrrr@gmail.com', '09752845782', 'scrypt:32768:8:1$5Jco7kbeQjG7HOh3$766cae1bceb624e6fb1e98343fe407d84edc2be70d1afa31cbb4b671288e1402d0061e52432e01a932e9e43e40bc3aa422d375a081bf411d9257dd6fb5dd1274', '2024-09-16 18:53:55', '8M.jpeg'),
(39, 'SUM2020-002650', 'Cucio', 'Julian', 'juliiiaaaannn@gmail.com', '09661972373', 'scrypt:32768:8:1$UuTqWUGgSjnWeoXC$0c77ba035f0ce5b4ac788efcf7621d407fed2994100374cb1e7e2ca3601716437c2844a85aff49d8fd5e5fa46132e1565dc619f8b67b66e61ce3b24862b5fdfa', '2024-09-16 18:57:09', 'julian.jpg'),
(51, 'SUM2021-006555', 'Dela Cruz', 'Juan', 'juandelacruz@gmail.com', '09764274590', 'scrypt:32768:8:1$UdzLs74Y5yOxSOwg$991cf69642e4d6c7b3c70f63be5507608731715d90dac532e0de2d0acb0d409ee47f01fb7f452255f3554f565f141deb19d8302281e28d8f86657e73d5923a4d', '2024-11-18 23:33:55', '173963e1.jpg');

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
(124, 33, 'Clocked In', '2024-11-13 22:00:42', 'Clocked In - User ID: 33', '2024-11-13 22:00:42'),
(125, 33, 'Clocked Out', '2024-11-13 22:01:55', 'Clocked Out - User ID: 33', '2024-11-13 22:01:55'),
(126, 33, 'Clocked In', '2024-11-13 22:02:00', 'Clocked In - User ID: 33', '2024-11-13 22:02:00'),
(127, 33, 'Clocked Out', '2024-11-13 22:02:05', 'Clocked Out - User ID: 33', '2024-11-13 22:02:05'),
(128, 33, 'Clocked In', '2024-11-13 22:05:03', 'Clocked In - User ID: 33', '2024-11-13 22:05:03'),
(129, 33, 'Clocked Out', '2024-11-13 22:05:07', 'Clocked Out - User ID: 33', '2024-11-13 22:05:07'),
(130, 37, 'Clocked In', '2024-11-13 22:05:38', 'Clocked In - User ID: 37', '2024-11-13 22:05:38'),
(132, 28, 'Clocked In', '2024-11-13 22:05:46', 'Clocked In - User ID: 28', '2024-11-13 22:05:46'),
(133, 38, 'Clocked In', '2024-11-13 22:05:49', 'Clocked In - User ID: 38', '2024-11-13 22:05:49'),
(134, 32, 'Clocked In', '2024-11-13 22:05:51', 'Clocked In - User ID: 32', '2024-11-13 22:05:51'),
(135, 32, 'Clocked Out', '2024-11-13 22:05:57', 'Clocked Out - User ID: 32', '2024-11-13 22:05:57'),
(136, 38, 'Clocked Out', '2024-11-13 22:06:00', 'Clocked Out - User ID: 38', '2024-11-13 22:06:00'),
(138, 37, 'Clocked Out', '2024-11-13 22:06:06', 'Clocked Out - User ID: 37', '2024-11-13 22:06:06'),
(139, 33, 'Clocked In', '2024-11-14 21:53:31', 'Clocked In - User ID: 33', '2024-11-14 21:53:31'),
(140, 33, 'Clocked Out', '2024-11-15 02:05:29', 'Clocked Out - User ID: 33', '2024-11-15 02:05:29'),
(141, 33, 'Clocked In', '2024-11-15 02:05:34', 'Clocked In - User ID: 33', '2024-11-15 02:05:34'),
(142, 33, 'Clocked Out', '2024-11-15 02:39:16', 'Clocked Out - User ID: 33', '2024-11-15 02:39:16'),
(143, 33, 'Clocked In', '2024-11-15 02:40:48', 'Clocked In - User ID: 33', '2024-11-15 02:40:48'),
(144, 33, 'Clocked Out', '2024-11-15 02:44:26', 'Clocked Out - User ID: 33', '2024-11-15 02:44:26'),
(145, 33, 'Clocked In', '2024-11-15 02:47:28', 'Clocked In - User ID: 33', '2024-11-15 02:47:28'),
(146, 33, 'Clocked Out', '2024-11-15 02:50:09', 'Clocked Out - User ID: 33', '2024-11-15 02:50:09'),
(147, 33, 'Clocked In', '2024-11-15 02:50:49', 'Clocked In - User ID: 33', '2024-11-15 02:50:49'),
(148, 33, 'Clocked Out', '2024-11-15 02:53:46', 'Clocked Out - User ID: 33', '2024-11-15 02:53:46'),
(149, 33, 'Clocked In', '2024-11-15 02:56:30', 'Clocked In - User ID: 33', '2024-11-15 02:56:30'),
(150, 33, 'Clocked Out', '2024-11-15 03:02:06', 'Clocked Out - User ID: 33', '2024-11-15 03:02:06'),
(151, 28, 'Login Successful', '2024-11-15 18:19:48', 'Login Successful - User ID: 28', '2024-11-15 18:19:48'),
(152, 28, 'Login successful', '2024-11-15 19:13:07', 'Login successful - User ID: 28', '2024-11-15 19:13:07'),
(153, 33, 'Clocked In', '2024-11-16 15:00:03', 'Clocked In - User ID: 33', '2024-11-16 15:00:03'),
(154, 32, 'Clocked In', '2024-11-16 15:02:52', 'Clocked In - User ID: 32', '2024-11-16 15:02:52'),
(155, 38, 'Clocked In', '2024-11-16 15:03:07', 'Clocked In - User ID: 38', '2024-11-16 15:03:07'),
(156, 28, 'Clocked In', '2024-11-16 15:03:19', 'Clocked In - User ID: 28', '2024-11-16 15:03:19'),
(158, 28, 'Clocked Out', '2024-11-16 15:38:39', 'Clocked Out - User ID: 28', '2024-11-16 15:38:39'),
(159, 28, 'Clocked In', '2024-11-16 17:07:53', 'Clocked In - User ID: 28', '2024-11-16 17:07:53'),
(160, 33, 'Clocked Out', '2024-11-16 17:43:08', 'Clocked Out - User ID: 33', '2024-11-16 17:43:08'),
(161, 28, 'Clocked Out', '2024-11-16 18:11:47', 'Clocked Out - User ID: 28', '2024-11-16 18:11:47'),
(162, 28, 'Clocked In', '2024-11-16 19:53:44', 'Clocked In - User ID: 28', '2024-11-16 19:53:44'),
(163, 28, 'Clocked Out', '2024-11-16 19:56:44', 'Clocked Out - User ID: 28', '2024-11-16 19:56:44'),
(164, 28, 'Clocked In', '2024-11-16 19:58:22', 'Clocked In - User ID: 28', '2024-11-16 19:58:22'),
(165, 28, 'Clocked Out', '2024-11-16 20:06:23', 'Clocked Out - User ID: 28', '2024-11-16 20:06:23'),
(166, 28, 'Clocked In', '2024-11-16 20:09:37', 'Clocked In - User ID: 28', '2024-11-16 20:09:37'),
(169, 28, 'Login successful', '2024-11-18 21:03:01', 'Login successful - User ID: 28', '2024-11-18 21:03:01'),
(170, 39, 'Login successful', '2024-11-18 21:13:27', 'Login successful - User ID: 39', '2024-11-18 21:13:27'),
(171, 28, 'Clocked In', '2024-11-18 21:46:12', 'Clocked In - User ID: 28', '2024-11-18 21:46:12'),
(172, 28, 'Clocked Out', '2024-11-18 21:47:48', 'Clocked Out - User ID: 28', '2024-11-18 21:47:48'),
(173, 28, 'Clocked In', '2024-11-18 21:56:59', 'Clocked In - User ID: 28', '2024-11-18 21:56:59'),
(174, 28, 'Clocked In', '2024-11-18 22:12:39', 'Clocked In - User ID: 28', '2024-11-18 22:12:39'),
(175, 28, 'Clocked In', '2024-11-18 22:13:33', 'Clocked In - User ID: 28', '2024-11-18 22:13:33'),
(176, 28, 'Clocked Out', '2024-11-18 22:35:27', 'Clocked Out - User ID: 28', '2024-11-18 22:35:27'),
(177, 28, 'Clocked In', '2024-11-18 22:38:22', 'Clocked In - User ID: 28', '2024-11-18 22:38:22'),
(178, 28, 'Clocked Out', '2024-11-18 22:39:08', 'Clocked Out - User ID: 28', '2024-11-18 22:39:08'),
(179, 28, 'Clocked In', '2024-11-18 22:39:23', 'Clocked In - User ID: 28', '2024-11-18 22:39:23'),
(180, 28, 'Clocked Out', '2024-11-18 22:40:02', 'Clocked Out - User ID: 28', '2024-11-18 22:40:02'),
(181, 28, 'Clocked In', '2024-11-18 22:41:17', 'Clocked In - User ID: 28', '2024-11-18 22:41:17'),
(182, 28, 'Clocked Out', '2024-11-18 22:42:07', 'Clocked Out - User ID: 28', '2024-11-18 22:42:07'),
(183, 28, 'Clocked In', '2024-11-18 22:44:40', 'Clocked In - User ID: 28', '2024-11-18 22:44:40'),
(184, 28, 'Clocked In', '2024-11-18 22:48:06', 'Clocked In - User ID: 28', '2024-11-18 22:48:06'),
(185, 28, 'Clocked Out', '2024-11-18 22:48:48', 'Clocked Out - User ID: 28', '2024-11-18 22:48:48'),
(186, 28, 'Clocked In', '2024-11-18 22:49:31', 'Clocked In - User ID: 28', '2024-11-18 22:49:31'),
(187, 28, 'Clocked In', '2024-11-18 22:49:57', 'Clocked In - User ID: 28', '2024-11-18 22:49:57'),
(188, 28, 'Login successful', '2024-11-18 23:01:10', 'Login successful - User ID: 28', '2024-11-18 23:01:10'),
(189, 51, 'Login successful', '2024-11-18 23:34:32', 'Login successful - User ID: 51', '2024-11-18 23:34:32'),
(190, 51, 'Added vehicle with Make: BMW, Model: 5 Series, RFID Number: 0004290568', '2024-11-18 23:35:59', 'Added vehicle with Make: BMW, Model: 5 Series, RFID Number: 0004290568 - User ID: 51', '2024-11-18 23:35:59'),
(191, 28, 'Clocked In', '2024-11-18 23:42:18', 'Clocked In - User ID: 28', '2024-11-18 23:42:18'),
(192, 28, 'Clocked Out', '2024-11-19 01:56:12', 'Clocked Out - User ID: 28', '2024-11-19 01:56:12'),
(193, 28, 'Clocked In', '2024-11-19 01:56:32', 'Clocked In - User ID: 28', '2024-11-19 01:56:32'),
(194, 28, 'Clocked Out', '2024-11-19 02:03:00', 'Clocked Out - User ID: 28', '2024-11-19 02:03:00'),
(195, 28, 'Clocked In', '2024-11-19 02:04:49', 'Clocked In - User ID: 28', '2024-11-19 02:04:49'),
(196, 28, 'Login successful', '2024-11-19 16:52:13', 'Login successful - User ID: 28', '2024-11-19 16:52:13'),
(197, 28, 'Clocked In', '2024-11-23 14:24:56', 'Clocked In - User ID: 28', '2024-11-23 14:24:56'),
(198, 28, 'Login successful', '2024-11-23 14:28:14', 'Login successful - User ID: 28', '2024-11-23 14:28:14');

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
(84, 28, 'CAX 3200', 'Cadillac', 'CTS', '2024-09-23 01:46:34'),
(85, 38, 'COR 2934', 'Bentley', 'Mulsanne', '2024-09-23 01:47:21'),
(86, 37, 'DJW 2394', 'Ford', 'Focus', '2024-09-23 01:47:45'),
(87, 33, 'SHE 2456', 'Suzuki', 'Swift', '2024-09-23 01:48:13'),
(88, 28, 'CCA 2945', 'BMW', 'X6 M', '2024-09-23 01:48:42'),
(90, 32, 'ROE 2945', 'Ferrari', 'California', '2024-09-23 01:49:24'),
(98, 51, 'VIN2934', 'BMW', '5 Series', '2024-11-18 23:35:59');

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
  ADD UNIQUE KEY `licenseplate_2` (`licenseplate`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `admin_activity_log`
--
ALTER TABLE `admin_activity_log`
  MODIFY `activity_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=198;

--
-- AUTO_INCREMENT for table `rfid`
--
ALTER TABLE `rfid`
  MODIFY `rfid_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=103;

--
-- AUTO_INCREMENT for table `time_logs`
--
ALTER TABLE `time_logs`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=84;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `user_activity_log`
--
ALTER TABLE `user_activity_log`
  MODIFY `activity_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=199;

--
-- AUTO_INCREMENT for table `vehicle`
--
ALTER TABLE `vehicle`
  MODIFY `vehicle_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=99;

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
