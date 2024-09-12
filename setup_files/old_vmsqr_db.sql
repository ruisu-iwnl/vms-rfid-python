-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 14, 2024 at 06:19 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vmsdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `adminID` int(11) NOT NULL,
  `employeeID` int(11) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `contactnumber` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`adminID`, `employeeID`, `lastname`, `firstname`, `contactnumber`, `email`, `password`) VALUES
(1, 1238, 'Pelaez', 'Emanuel Luis', 2147483647, 'herroin29@gmail.com', 'scrypt:32768:8:1$FeVYPYkeZqdCJhiR$d657bd4b818992de84f33507b1cc245b0176ed9084b3a2a6ca5c593278d415bb7e640aceb199bdbaa9af26fd99620a9e8654e0fb93744ec17812702715c1816b');

-- --------------------------------------------------------

--
-- Table structure for table `qr_codes`
--

CREATE TABLE `qr_codes` (
  `qr_id` int(11) NOT NULL,
  `userID` int(255) NOT NULL,
  `qr_code_image` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `qr_codes`
--

INSERT INTO `qr_codes` (`qr_id`, `userID`, `qr_code_image`) VALUES
(1, 1, 'iVBORw0KGgoAAAANSUhEUgAAAeoAAAHqAQAAAADjFjCXAAAECUlEQVR4nO2dTW6jXBBFTzVIHoLUC8hS8M6iXlJ2AEvJDmAYyah6UO8H0t8IaHXy+dYAOcZHz5auql79PGLOCZt+nKFBuHDhwoULFy5c+LW4JWsBVgNW29h9SS9gKe9dt7rwJ8UHd3efwe7Lze2+tLi7e9z41QPD3DjQeNy4cnXhT4Zncc2ErnzM723ENcxZa0V6IcfxW/924V8FtzuNM/Vg1q/mPjfO1K/G1IOPf3d14c+Bt5/+dpbeGN7bh7O0GN0DB7BhXluGt0tXF/6ceFZd58ACRucw9ZjTOTa8tQ8b3nqc5acbwLau/K1/u/B/jE9mZtYDw3uLvc5NpBTZGrd7vFpzNnvh6sKfDA9hVfflLADdI12ml48opOQb+w7at/7twv8Vzi5VTZdIZMeokjxwn4niCnQPfOweKc1VDiv8kCXVhXNzz5JKl1AiXX3lHhdVToQft0/1OgZPwdVHmlSgS/4vVfNCnfJ1wo9brf6Gc6slYI+icVZduL4SZqU64cctyYfdbm6sgTSaEblAHHFVvQnh52zj68a8X4NdNE27vmrdA6lO+AmrOWx0v2AbayPM+gw+dq59nfBL8BJhm01uWnOIpLA56Q92n5PqhB+zFGEjfQBCV+XuGAW6fUllRtmE8Cvw1cxe3KH7SJMmwwz2OoO9vqfemN1p3O51m/dFvrzw74inuc0QVx5tiqLxcgslxg2WFlhumuoUfsZSXhA57IOaPuR6canmzXVLp3qd8FPmxVIxeIba/f+UQ8QOT/s64efwnepyNpscXlWiJw+365xJdcKPWhVXHTfJ7f4ml+VqWbhMCcjXCT9uWVe5NjJCKZA0m3pJ9XUpzEp1wk/iw7xazU3N7Jb7YEsLUw/ptE7nOZG9cHXhT4aXjlgZciL3xsrME6k3xnYYSvs64Ydtd0Zs+VnaEqsxWeNM95sTE+w0D6a+iXF3v2R14U+N15HhyVrs3qXGV+pDlNB7h4i18eprfHnh3w3fTDqlN7o62pTjKpSZk0gkFGGFn7K8ryud/jy37uXwxPYjkB+KItUJP2w7X1cenVN6Y+WgWBqBqoN3Up3ww1ZVl4RUD0pE4zWV6qoc1YcVfpHqPAfXMl+XBtqL9GLDB4qwwi/sw27055vkopwby91X9WGFX5dNsBlPn8mur3PfDD4V1ydfJ/w0HkFzBh8XMx8Be51X83FJ5btkxfVdubrwJ8P/8+x/areWuEpX30P7OuGXdsQAWHosPTWxN6aXD3PAbXg3HNbWWXp1xIRfizfuI+ncBNB4PCv2Vw+w3OJJdnb/S6sLfwJ8fzKxpqq5LTFSHnFSzk0omxB+Dv8jh63jTmPNZjvPM59lqliqE37YTP+9Trhw4cKFCxcu/H+B/wYetVNJUeZGSQAAAABJRU5ErkJggg=='),
(2, 2, 'iVBORw0KGgoAAAANSUhEUgAAAeoAAAHqAQAAAADjFjCXAAAEKUlEQVR4nO2dXarcOBBGT40N/WjDLCBLce8sZEnZgb2UXkDAfmywqXmQSlYnZAZsDzeX/urhYrp1UBs+Sqof6Zpzwqa/ztAgXLhw4cKFCxcu/FrcsrXYHWAyMyZr0xi7pyEtdl9i6P262YW/G467uzO4u/vcuPsM0Lm7+wrQOBBfDHPjFTF+6ncX/tH4Eu5r6sFHNrN7Etxm0K2kbyF7vWtnF/5eePvrR81qcHOm/kcL3YwBMH3x/HTd7MKFJ+tWGNLiCj4uLe6PFljsF9H9cT9e+KfAw9d1DizA8GhXn/qZ5PBgM6db8enerLBAnVf+1O8u/KPwHE1ka5xh/vc/MVTRhPDDlnxd5b6mHmP6suKwAmzmU9/gLJB94mWzC39PPHxdt+a0yNjlHAp0K+4zuPsaGRZlToSfx0u+bsXHrqgpiTALLjQJWY5k6Ul1wo9Z1s/cuI9A+DqS68uDuqLJGXyU6oSfsyyfLhyel8ghBxeE/vaUSnqS6oQftBRNGB0wWeNMd8xZNnOW3qBbW+iexvD95kwGDttFswt/T7ze15W1dl9SUyAxpqFNGsegaEL4JfjSkppMpp4UudrXeTOzfhfh0/xb/7/MLvy98MrXpf0aETREHwrh3ErSpGDydcKPWeTrPGdExuTX1pKlW0vQGjFESd9JdcLP4MPDzN2fBsvN04LL0mJ3Grd7anwitXtaboG6bnbhb4bX+TqfKZEDRG4uUsU5kVwWYfk64YftJXKNjVze3OXMXV5w57o2IdUJP2Ghuhy51mkRdjfnRXqNqzYh/KLaBLDXJrLW5lL9mqESZoV96ncX/lH4Sy/J3kbnefuWN3JEgXYssa5UJ/y4ebGcDC7ObXzZ3IUIvSpQSHXCD1muww7f/15TqmRwgG5tbXhY9HKymadxD8OhcbtkduHvjXdPS4EEixlTD5E5zicTmazFv/WN62Si8KtW2H1xbaL6MBPHrmfqWKPq/vzU7y78g/HJbg7d08x6sPtyy2k5umfcLrHcPDvBRb5O+CmLGLbO1+VESnUBRTk3sRcy5OuEH7YIX70qQSQbog621/yj+wTFsMLP2K666FYvXm+GyKZAVRbTvk74RfhmSXpT37hZD6Rk8OOW+0uGGezeuWtfJ/wiX0e0mwyRLya12xHnYUuVIpl8nfDj5q8WCZKXwmt1eMxfDllIdcIP2e7rKM5tr42lIeWz/ciiVCf8NJ4zIuXpdTf3da7lmAoZV84u/E3xuKvTrN/MrN+sur8p1csebb6wOLe2Xzi78PfCqyxx1Ty836kzRuZkDzPU1Sn8JP7zDbEOT2MY1xaWHoZYa32yZnXAje6H+SWzC39P/OdKV9wfVl+TGO4wCv86NyH8HP7rXZ1FhHvf8Eh9gmI/jy3VCT9k5v895vem/14nXLhw4cKFCxf+p+D/AKkvRMaV5WJTAAAAAElFTkSuQmCC');

-- --------------------------------------------------------

--
-- Table structure for table `time_logs`
--

CREATE TABLE `time_logs` (
  `logID` int(11) NOT NULL,
  `userID` int(11) NOT NULL,
  `time_in` datetime NOT NULL,
  `time_out` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `time_logs`
--

INSERT INTO `time_logs` (`logID`, `userID`, `time_in`, `time_out`) VALUES
(1, 1, '2024-04-14 21:57:08', '2024-04-14 21:57:29'),
(2, 2, '2024-04-14 21:58:37', '2024-04-14 21:58:39'),
(3, 1, '2024-04-14 21:57:08', '2024-04-14 21:57:29'),
(4, 2, '2024-04-14 21:58:37', '2024-04-14 21:58:39'),
(5, 2, '2024-04-14 21:58:37', '2024-04-14 21:58:39');

-- --------------------------------------------------------

--
-- Table structure for table `time_logs_history`
--

CREATE TABLE `time_logs_history` (
  `logID` int(11) NOT NULL,
  `userID` int(11) NOT NULL,
  `time_in` datetime NOT NULL,
  `time_out` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `userID` int(11) NOT NULL,
  `infoID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userID`, `infoID`) VALUES
(1, 1),
(2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `userinfo`
--

CREATE TABLE `userinfo` (
  `infoID` int(11) NOT NULL,
  `studno` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `contactnumber` varchar(11) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `userinfo`
--

INSERT INTO `userinfo` (`infoID`, `studno`, `lastname`, `firstname`, `email`, `contactnumber`, `password`) VALUES
(1, 'SUM2021-00366', 'Pelaez', 'Lowis', 'e.luis.pelaez@gmail.com', '09764274590', 'scrypt:32768:8:1$lX6Dyee9DsDG4O8Z$9aa614def3a480b20632d4e486167a32c46ef494d64d347c2ed523fac29d1381a5ed205c6a705f37e8b06fcbfcc70a78ee2867fcc31f76a24a96b2adeda4cd20'),
(2, '20130513-023485', 'Dela Cruz', 'Juan', 'e.lu1s@yahoo.com', '09672849927', 'scrypt:32768:8:1$F2JpuuznLWvOIQsv$c4bc58095e5b83236cc78712234f32bc00250def90b544e17a028b971f6ef73de423e87dc53d2eb41418b8b52506c08eadb7ec0079c0248f9de9027f2e83c26a');

--
-- Triggers `userinfo`
--
DELIMITER $$
CREATE TRIGGER `after_userinfo_insert` AFTER INSERT ON `userinfo` FOR EACH ROW BEGIN
    INSERT INTO user (infoID) VALUES (NEW.infoID);
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `delete_qr_codes_cascade` BEFORE DELETE ON `userinfo` FOR EACH ROW BEGIN
    DELETE FROM `qr_codes` WHERE `userID` IN (SELECT `userID` FROM `user` WHERE `infoID` = OLD.infoID);
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `delete_user_cascade` BEFORE DELETE ON `userinfo` FOR EACH ROW BEGIN
    DELETE FROM `user` WHERE `infoID` = OLD.infoID;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `delete_vehicle_cascade` BEFORE DELETE ON `userinfo` FOR EACH ROW BEGIN
    DELETE FROM `vehicle` WHERE `userID` IN (SELECT `userID` FROM `user` WHERE `infoID` = OLD.infoID);
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `vehicle`
--

CREATE TABLE `vehicle` (
  `vehicleID` int(11) NOT NULL,
  `userID` int(11) NOT NULL,
  `licenseplate` varchar(255) NOT NULL,
  `model` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicle`
--

INSERT INTO `vehicle` (`vehicleID`, `userID`, `licenseplate`, `model`) VALUES
(1, 1, 'LUI 0529', 'Mazda Miata MX-5'),
(2, 2, 'JDC 2839', 'Ford Mustang Coupe'),
(3, 2, 'TES 9245', 'Tesla Cybertruck'),
(4, 2, 'LET 2814', 'Honda Civic'),
(5, 1, 'EVL 3384', '1974 Oldsmobile Delta 88'),
(6, 1, 'GDF 1966', '1966 Chevrolet Corvette'),
(7, 1, 'GDF 1979', '1979 Cadillac Coupe DeVille'),
(8, 1, 'RYL 2983', '1980 Volvo 244');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`adminID`),
  ADD UNIQUE KEY `username` (`email`);

--
-- Indexes for table `qr_codes`
--
ALTER TABLE `qr_codes`
  ADD PRIMARY KEY (`qr_id`),
  ADD UNIQUE KEY `user_id` (`userID`);

--
-- Indexes for table `time_logs`
--
ALTER TABLE `time_logs`
  ADD PRIMARY KEY (`logID`),
  ADD KEY `fk_user_time_logs` (`userID`);

--
-- Indexes for table `time_logs_history`
--
ALTER TABLE `time_logs_history`
  ADD PRIMARY KEY (`logID`),
  ADD KEY `fk_user_time_logs_history` (`userID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userID`),
  ADD UNIQUE KEY `infoID` (`infoID`);

--
-- Indexes for table `userinfo`
--
ALTER TABLE `userinfo`
  ADD PRIMARY KEY (`infoID`),
  ADD UNIQUE KEY `unique_email` (`email`);

--
-- Indexes for table `vehicle`
--
ALTER TABLE `vehicle`
  ADD PRIMARY KEY (`vehicleID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `adminID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `qr_codes`
--
ALTER TABLE `qr_codes`
  MODIFY `qr_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `time_logs`
--
ALTER TABLE `time_logs`
  MODIFY `logID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `userID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `userinfo`
--
ALTER TABLE `userinfo`
  MODIFY `infoID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `vehicle`
--
ALTER TABLE `vehicle`
  MODIFY `vehicleID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `qr_codes`
--
ALTER TABLE `qr_codes`
  ADD CONSTRAINT `fk_user_qr` FOREIGN KEY (`userID`) REFERENCES `user` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `time_logs`
--
ALTER TABLE `time_logs`
  ADD CONSTRAINT `fk_user_time_logs` FOREIGN KEY (`userID`) REFERENCES `user` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `time_logs_history`
--
ALTER TABLE `time_logs_history`
  ADD CONSTRAINT `fk_user_time_logs_history` FOREIGN KEY (`userID`) REFERENCES `user` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `infoID` FOREIGN KEY (`infoID`) REFERENCES `userinfo` (`infoID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
