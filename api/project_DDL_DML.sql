drop database if exists carmaster_db;
create database carmaster_db;

use carmaster_db;

-- ============================================
-- 자동차 신규등록 통계 코드 테이블 DDL
-- ============================================

-- 1. 차종코드 테이블
CREATE TABLE IF NOT EXISTS code_vhcty_asort (
    code VARCHAR(1) PRIMARY KEY COMMENT '차종코드',
    name VARCHAR(10) NOT NULL COMMENT '차종명'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='차종코드';

-- 2. 등록지역코드 테이블
CREATE TABLE IF NOT EXISTS code_regist_grc (
    code VARCHAR(2) PRIMARY KEY COMMENT '등록지역코드',
    name VARCHAR(10) NOT NULL COMMENT '지역명'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='등록지역코드';

-- 3. 사용연료코드 테이블
CREATE TABLE IF NOT EXISTS code_use_fuel (
    code VARCHAR(2) PRIMARY KEY COMMENT '사용연료코드',
    name VARCHAR(30) NOT NULL COMMENT '연료명'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='사용연료코드';

-- 4. 용도구분코드 테이블
CREATE TABLE IF NOT EXISTS code_prpos_se (
    code VARCHAR(1) PRIMARY KEY COMMENT '용도구분코드',
    name VARCHAR(10) NOT NULL COMMENT '용도명'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='용도구분코드';

-- 5. 성별구분코드 테이블
CREATE TABLE IF NOT EXISTS code_sexdstn (
    code VARCHAR(10) PRIMARY KEY COMMENT '성별구분코드',
    name VARCHAR(10) NOT NULL COMMENT '성별명'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='성별구분코드';

-- 6. 연령대코드 테이블
CREATE TABLE IF NOT EXISTS code_agrde (
    code VARCHAR(1) PRIMARY KEY COMMENT '연령대코드',
    name VARCHAR(10) NOT NULL COMMENT '연령대명'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='연령대코드';

-- 7. 배기량코드 테이블
CREATE TABLE IF NOT EXISTS code_dsplvl (
    code VARCHAR(2) PRIMARY KEY COMMENT '배기량코드',
    name VARCHAR(20) NOT NULL COMMENT '배기량명'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='배기량코드';

-- 8. 국산수입구분코드 테이블
CREATE TABLE IF NOT EXISTS code_hmmd_imp (
    code VARCHAR(10) PRIMARY KEY COMMENT '국산수입구분코드',
    name VARCHAR(10) NOT NULL COMMENT '구분명'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='국산수입구분코드';

-- 메인 테이블 (이미 생성된 경우 스킵)
CREATE TABLE IF NOT EXISTS car_registration_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    regist_yy VARCHAR(4) NOT NULL COMMENT '등록년',
    regist_mt VARCHAR(2) NOT NULL COMMENT '등록월',
    vhcty_asort_code VARCHAR(1) COMMENT '차종코드',
    regist_grc_code VARCHAR(2) COMMENT '등록지역코드',
    use_fuel_code VARCHAR(2) COMMENT '사용연료코드',
    cnm_code VARCHAR(6) COMMENT '차명코드',
    prpos_se_code VARCHAR(1) COMMENT '용도구분코드',
    sexdstn VARCHAR(10) COMMENT '성별구분',
    agrde VARCHAR(1) COMMENT '연령대코드',
    dsplvl_code VARCHAR(2) COMMENT '배기량코드',
    hmmd_imp_se_nm VARCHAR(10) COMMENT '국산수입구분명',
    prye VARCHAR(4) COMMENT '모델년도',
    cnt INT DEFAULT 0 COMMENT '등록대수',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_regist_ym (regist_yy, regist_mt),
    INDEX idx_vhcty (vhcty_asort_code),
    INDEX idx_region (regist_grc_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='자동차 신규등록 통계';

-- ============================================
-- 자동차 신규등록 통계 코드 테이블 초기 데이터 DML
-- ============================================

-- 1. 차종코드 데이터
INSERT INTO code_vhcty_asort (code, name) VALUES
('1', '승용'),
('2', '승합'),
('3', '화물'),
('4', '특수');

-- 2. 등록지역코드 데이터
INSERT INTO code_regist_grc (code, name) VALUES
('1', '서울'),
('2', '부산'),
('3', '대구'),
('4', '인천'),
('5', '광주'),
('6', '대전'),
('7', '울산'),
('8', '세종'),
('9', '경기'),
('10', '강원'),
('11', '충북'),
('12', '충남'),
('13', '전북'),
('14', '전남'),
('15', '경북'),
('16', '경남'),
('17', '제주');

-- 3. 사용연료코드 데이터
INSERT INTO code_use_fuel (code, name) VALUES
('1', 'CNG'),
('2', '경유'),
('3', '수소'),
('4', '엘피지'),
('5', '전기'),
('6', '하이브리드(CNG+전기)'),
('7', '하이브리드(휘발유+전기)'),
('8', '휘발유'),
('9', '휘발유(무연)'),
('10', '휘발유(유연)'),
('11', '기타연료');

-- 4. 용도구분코드 데이터
INSERT INTO code_prpos_se (code, name) VALUES
('1', '자가용'),
('2', '영업용'),
('3', '관용');

-- 5. 성별구분코드 데이터
INSERT INTO code_sexdstn (code, name) VALUES
('남자', '남자'),
('여자', '여자'),
('법인', '법인');

-- 6. 연령대코드 데이터
INSERT INTO code_agrde (code, name) VALUES
('0', '법인'),
('1', '10대'),
('2', '20대'),
('3', '30대'),
('4', '40대'),
('5', '50대'),
('6', '60대'),
('7', '70대'),
('8', '80대');

-- 7. 배기량코드 데이터
INSERT INTO code_dsplvl (code, name) VALUES
('1', '800cc미만'),
('2', '1000cc미만'),
('3', '1500cc미만'),
('4', '2000cc미만'),
('5', '2500cc미만'),
('6', '3000cc미만'),
('7', '3500cc미만'),
('8', '4000cc미만'),
('9', '4500cc미만'),
('10', '5000cc미만'),
('11', '5000cc이상');

-- 8. 국산수입구분코드 데이터
INSERT INTO code_hmmd_imp (code, name) VALUES
('국산', '국산'),
('외산', '외산');

