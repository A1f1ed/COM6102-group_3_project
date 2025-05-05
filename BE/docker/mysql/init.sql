
-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS COM6102;
USE COM6102;


DROP USER IF EXISTS 'seatunnel'@'%';
CREATE USER 'seatunnel'@'%' IDENTIFIED BY '123456';
GRANT SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE, REPLICATION CLIENT, LOCK TABLES ON *.* TO 'seatunnel'@'%';
GRANT ALL PRIVILEGES ON COM6102.* TO 'seatunnel'@'%';

DROP USER IF EXISTS 'Jerry'@'%';
CREATE USER 'Jerry'@'%' IDENTIFIED BY '123456';
GRANT SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE, REPLICATION CLIENT, LOCK TABLES ON *.* TO 'Jerry'@'%';
GRANT ALL PRIVILEGES ON COM6102.* TO 'Jerry'@'%';


FLUSH PRIVILEGES;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nickName VARCHAR(50) DEFAULT '',
    phoneNum INT,
    userImg VARCHAR(255) DEFAULT 'http://newcoffee.wwp666.cn:10006/assets/default.png',
    userBg VARCHAR(255) DEFAULT 'http://newcoffee.wwp666.cn:10006/assets/default_bg.jpg',
    `desc` TEXT,
    vip INT DEFAULT 0,
    token VARCHAR(255),
    token_expire DATETIME,
    createdAt DATETIME NOT NULL,
    updatedAt DATETIME NOT NULL
);

-- 创建商品类型表
CREATE TABLE IF NOT EXISTS product_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type VARCHAR(20) UNIQUE NOT NULL,
    typeDesc VARCHAR(20) NOT NULL,
    createdAt DATETIME NOT NULL,
    updatedAt DATETIME NOT NULL
);

-- 创建商品表
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pid VARCHAR(20) UNIQUE NOT NULL,
    type VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    enname VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    `desc` TEXT NOT NULL,
    smallImg VARCHAR(255) NOT NULL,
    largeImg VARCHAR(255) NOT NULL,
    isHot INT DEFAULT 0,
    tem VARCHAR(50),
    tem_desc VARCHAR(50),
    sugar VARCHAR(50),
    sugar_desc VARCHAR(50),
    milk VARCHAR(50),
    milk_desc VARCHAR(50),
    cream VARCHAR(50),
    cream_desc VARCHAR(50),
    createdAt DATETIME NOT NULL,
    updatedAt DATETIME NOT NULL,
    FOREIGN KEY (type) REFERENCES product_types(type)
);

-- 创建推广表
CREATE TABLE IF NOT EXISTS promotions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    imgUrl VARCHAR(255) NOT NULL,
    `desc` VARCHAR(255) NOT NULL,
    sort_order INT DEFAULT 0,
    createdAt DATETIME NOT NULL,
    updatedAt DATETIME NOT NULL
);




-- 插入商品分类数据
INSERT INTO product_types (id, type, typeDesc, createdAt, updatedAt) VALUES
(1, 'latte', '拿铁', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(2, 'rena_ice', '瑞纳冰', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(3, 'coffee', '咖啡', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(4, 'fruit_tea', '水果茶', '2024-11-18 07:22:51', '2024-11-18 07:22:51');

-- 插入商品数据
-- 拿铁类商品
INSERT INTO products (id, pid, type, name, enname, price, `desc`, smallImg, largeImg, isHot, tem, tem_desc, sugar, sugar_desc, milk, milk_desc, cream, cream_desc, createdAt, updatedAt) VALUES
(1, 'latte001', 'latte', '黑糖拿铁', 'Brown Sugar Latte', 28.00, '经典日式黑糖风味拿铁，黑糖与咖啡的美妙融合，香甜温暖、自然醇厚，口感绵长。（建议到店饮用，奶油融化前口感更佳）\n 主要原材料：浓缩咖啡、牛奶、黑糖调味糖浆、原味调味糖浆、可选择添加搅打奶油（含香草风味糖浆）\n 图片仅供参考，请以实物为准，建议取餐后尽快饮用。', 'http://newcoffee.wwp666.cn:10006/images/product_small/IMG_0378_02p.jpg', 'http://newcoffee.wwp666.cn:10006/images/product_large/IMG_0378_02.jpg', 0, '冷/热', '温度', '全糖/半糖', '糖', '', '奶', '默认奶油/无奶油', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(2, 'latte002', 'latte', '香草拿铁', 'Vanilla Latte', 28.00, '拿铁中融入清新香草风味，沁人心脾。\n主要原材料：浓缩咖啡，牛奶，香草风味糖浆。\n图片仅供参考，请以实物为准。建议送达后尽快饮用。', 'http://newcoffee.wwp666.cn:10006/images/product_small/IMG_0379_02p.jpg', 'http://newcoffee.wwp666.cn:10006/images/product_large/IMG_0379_02.jpg', 0, '冷/热', '温度', '全糖/半糖', '糖', '', '奶', '', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(6, 'latte003', 'latte', '拿铁', 'Latte', 25.00, '经典意式奶咖。浓缩咖啡与香醇牛奶融合，口感圆润。\n主要原材料：浓缩咖啡，牛奶。\n图片仅供参考，请以实物为准。建议送达后尽快饮用。', 'http://newcoffee.wwp666.cn:10006/images/product_small/IMG_0383_02p.jpg', 'http://newcoffee.wwp666.cn:10006/images/product_large/IMG_0383_02.jpg', 0, '冷/热', '温度', '全糖/半糖', '糖', '', '奶', '', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(14, 'latte007', 'latte', '元气厚乳拿铁', 'Walnut Flavored Newer Latte', 21.00, '【新年第一杯，元气开场】香浓核桃风味×酥脆坚果碎稀奶油顶，给你加个元气buff！\n以luckin经典厚乳拿铁为底，新年要有新风味~特添精选厚乳，采用先进冷萃工艺，乳蛋白含量6%。\n主要原料：浓缩咖啡、冷萃厚牛乳（调制奶浆）、纯牛奶、胡桃风味糖浆、糖衣扁桃仁碎、稀奶油（含香草味糖浆）。\n图片及包装仅供参考，请以实物为准。建议送达后尽快饮用。到店饮用口感更佳。', 'http://newcoffee.wwp666.cn:10006/images/product_small/b001_small.jpg', 'http://newcoffee.wwp666.cn:10006/images/product_large/b001.jpg', 0, '冰/热', '温度', '标准糖/半糖', '糖', '', '奶', '默认奶油/无奶油', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(16, 'latte006', 'latte', '黑糖啵啵拿铁', 'Brown Sugar Bubble Latte', 28.00, '独特的黑糖风味拿铁，佐以Q嫩儒糯的黑糖口味珍珠，创造出层次丰富的美妙口感。（建议搅拌后饮用）\n主要原材料：浓缩咖啡，黑糖味珍珠，纯牛奶，黑糖味调味糖浆，原味调味糖浆，可选择添加搅打奶油（含香草风味糖浆）\n图片仅供参考，请以实物为准，建议取餐后尽快饮用。', 'http://newcoffee.wwp666.cn:10006/images/product_small/IMG_0392_02p.jpg', 'http://newcoffee.wwp666.cn:10006/images/product_large/IMG_0392_02.jpg', 1, '冷/热', '温度', '全糖/半糖', '糖', '', '奶', '默认奶油/无奶油', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(17, 'latte008', 'latte', '海盐芝士厚乳拿铁', 'Salty Cheese Newer Latte', 18.00, '【特添精选厚乳，采用先进冷萃工艺，乳蛋白含量6%】悉心拼配滑润醇香的厚乳拿铁，缓缓浇入轻盈绵密的海盐芝士奶盖，更添美妙风味。\n主要原料：浓缩咖啡、冷萃厚牛乳（调制奶浆）、纯牛奶、原味调味糖浆、海盐芝士奶盖风味固体饮料、稀奶油。\n图片及包装仅供参考，请以实物为准。建议送达后尽快饮用。到店饮用口感更佳。\n致敏物质：本产品含有乳及乳制品、大豆制品，对此有过敏历史的小伙伴注意哦～', 'http://newcoffee.wwp666.cn:10006/images/product_small/c001_small.jpg', 'http://newcoffee.wwp666.cn:10006/images/product_large/c001.jpg', 0, '冰/热', '温度', '标准糖/半糖/无糖', '糖', '', '奶', '', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(21, 'latte009', 'latte', '茴香拿铁', 'Anise latte', 22.00, '平滑、香甜、细致的花香，这款诱人的拿铁咖啡定会愉悦您的味蕾，活跃您的感官。主要原料：1颗 Master Origin Ethiopia 优选咖啡、250毫升牛奶、20毫升大茴香糖浆、绿茉莉花茶包、大茴香瓣。\n图片及包装仅供参考，请以实物为准。建议送达后尽快饮用。到店饮用口感更佳。', 'http://newcoffee.wwp666.cn:10006/images/product_small/i001_small.png', 'http://newcoffee.wwp666.cn:10006/images/product_large/i001.jpg', 0, '冰/热', '温度', '标准糖/半糖/无糖', '糖', '', '奶', '', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
-- 咖啡类商品
(3, 'coffee002', 'coffee', '焦糖玛奇朵', 'Caramel Macchiato', 28.00, '焦糖风味奶咖，上层注入丰富奶泡，层次感分明。（建议到店饮用）\n主要原材料：浓缩咖啡，牛奶，香草风味糖浆，焦糖调味酱。\n图片仅供参考，请以实物为准。建议送达后尽快饮用。', 'http://newcoffee.wwp666.cn:10006/images/product_small/IMG_0381_02p.jpg', 'http://newcoffee.wwp666.cn:10006/images/product_large/IMG_0381_02.jpg', 0, '冷/热', '温度', '全糖/半糖', '糖', '', '奶', '', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(4, 'coffee001', 'coffee', '标准美式', 'Americano', 22.00, 'Espresso（意式浓缩）与水的黄金配比，带来浓郁的咖啡芬芳，成为脑海中挥之不去的绝妙体验。\n主要原材料：浓缩咖啡，水。\n图片仅供参考，请以实物为准。建议送达后尽快饮用。', 'http://newcoffee.wwp666.cn:10006/images/product_small/IMG_0380_02p.jpg', 'http://newcoffee.wwp666.cn:10006/images/product_large/IMG_0380_02.jpg', 0, '冷/热', '温度', '无糖/半份糖/单份糖', '糖', '', '奶', '', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(5, 'coffee003', 'coffee', '摩卡', 'Mocha', 28.00, '浓缩咖啡与牛奶彼此融合，加入香浓巧克力风味。（建议到店饮用，奶油融化前口感更佳）\n主要原材料：浓缩咖啡，牛奶，巧克力酱，搅打奶油（含香草风味糖浆）。\n图片仅供参考，请以实物为准。建议送达后尽快饮用。', 'http://newcoffee.wwp666.cn:10006/images/product_small/IMG_0382_02p.jpg', 'http://newcoffee.wwp666.cn:10006/images/product_large/IMG_0382_02.jpg', 0, '冷/热', '温度', '全糖/半糖', '糖', '', '奶', '默认奶油/无奶油', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(7, 'latte004', 'coffee', '焦糖拿铁', 'Caramel Latte', 28.00, '拿铁中融入醇香焦糖风味，香甜温暖，令人沉醉。\n主要原材料：浓缩咖啡，牛奶，焦糖风味糖浆。\n图片仅供参考，请以实物为准。建议送达后尽快饮用。', 'http://newcoffee.wwp666.cn:10006/images/product_small/IMG_0384_02p.jpg', 'http://newcoffee.wwp666.cn:10006/images/product_large/IMG_0384_02.jpg', 1, '冷/热', '温度', '全糖/半糖', '糖', '', '奶', '', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(8, 'latte005', 'coffee', '榛果拿铁', 'Hazelnut Latte', 28.00, '榛果爱好者的选择！香甜榛果风味与咖啡牛奶融合，诠释另一种新鲜风味。\n主要原材料：浓缩咖啡，牛奶，榛子风味糖浆。\n图片仅供参考，请以实物为准。建议送达后尽快饮用。', 'http://newcoffee.wwp666.cn:10006/images/product_small/IMG_0385_02p.jpg', 'http://newcoffee.wwp666.cn:10006/images/product_large/IMG_0385_02.jpg', 1, '冷/热', '温度', '全糖/半糖', '糖', '', '奶', '', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
-- 瑞纳冰类商品
(9, 'rena_ice001', 'rena_ice', '巧克力瑞纳冰', 'Chocolate Exfreezo', 28.00, '醇香巧克力风味搭配牛奶，口感香甜酷爽。（到店饮用口感更佳）\n主要原料：巧克力酱，牛奶，冰沙粉，冰块，搅打奶油（含香草风味糖浆）。\n图片仅供参考，请以实物为准。建议送达后尽快饮用。', 'http://newcoffee.wwp666.cn:10006/images/product_small/IMG_0387_02p.jpg', 'http://newcoffee.wwp666.cn:10006/images/product_large/IMG_0387_02.jpg', 0, '', '温度', '', '糖', '', '奶', '默认奶油/无奶油', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(11, 'rena_ice002', 'rena_ice', '抹茶瑞纳冰', 'Matcha Exfreezo', 28.00, '经典抹茶搭配香滑奶油，入口伴有浓郁的抹茶清香。（到店饮用口感更佳）\n主要原料：抹茶风味固体饮料，冰沙粉，牛奶，冰块，搅打稀奶油。\n图片仅供参考，请以实物为准。建议送达后尽快饮用。', 'http://newcoffee.wwp666.cn:10006/images/product_small/IMG_0388_02p.jpg', 'http://newcoffee.wwp666.cn:10006/images/product_large/IMG_0388_02.jpg', 0, '', '温度', '', '糖', '', '奶', '默认奶油/无奶油', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(12, 'rena_ice003', 'rena_ice', '卡布奇诺瑞纳冰', 'Coppuccino Exfreezo', 28.00, '卡布奇诺咖啡风味融入牛奶与细腻沙冰，香甜纯滑。（到店饮用口感更佳）\n主要原料：卡布奇诺咖啡风味冰沙粉，牛奶，冰沙粉，冰块，搅打奶油（含香草风味糖浆）。\n图片仅供参考，请以实物为准。建议送达后尽快饮用。', 'http://newcoffee.wwp666.cn:10006/images/product_small/IMG_0389_02p.jpg', 'http://newcoffee.wwp666.cn:10006/images/product_large/IMG_0389_02.jpg', 0, '', '温度', '', '糖', '', '奶', '默认奶油/无奶油', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51');

-- 水果茶类商品
INSERT INTO products (id, pid, type, name, enname, price, `desc`, smallImg, largeImg, isHot, tem, tem_desc, sugar, sugar_desc, milk, milk_desc, cream, cream_desc, createdAt, updatedAt) VALUES
(18, 'fruit_tea002', 'fruit_tea', '草莓酸饮', 'Strawberry sour drink', 19.00, '草莓和椰果的酸甜搭配，混合醇香牛奶与清新优格，交织出Q滑细腻的口感，莓香四溢很好喝。（饮用前建议搅拌）\n主要原材料：牛奶、草莓汁饮料浓浆、椰果、风味酸奶。\n图片仅供参考，请以实物为准，建议取餐后尽快饮用。', 'http://newcoffee.wwp666.cn:10006/images/product_small/e001_small.png', 'http://newcoffee.wwp666.cn:10006/images/product_large/e001.png', 0, '冰', '温度', '标准/半糖/0卡糖', '糖', '', '奶', '', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(19, 'fruit_tea001', 'fruit_tea', '满杯百香果', 'Passion Fruit & Coconut Jelly Jasmine Tea', 17.00, '清新又浓郁的百香果香气，混合清新茉莉茶香，加上椰果与寒天的爽滑Q弹，满杯椰香果香茶香。\n主要原材料：椰果、百香果汁、原味寒天晶球、茉莉绿茶、原味调味糖浆。\n图片仅供参考，请以实物为准，建议取餐后尽快饮用。', 'http://newcoffee.wwp666.cn:10006/images/product_small/d001_small.png', 'http://newcoffee.wwp666.cn:10006/images/product_large/d001.png', 1, '冰', '温度', '标准/半糖/0卡糖', '糖', '', '奶', '', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
(20, 'fruit_tea005', 'fruit_tea', '椰子冰', 'Coconut ice', 20.00, '【不含咖啡】优选纯牛奶为底，融进满满椰香，又加入柔和香草风味，椰子控必喝。\n主要原料：纯牛奶、椰子风味粉、香草风味糖浆、原味冰沙粉、冰块、稀奶油（含香草风味糖浆）。\n图片及包装仅供参考，请以实物为准。温馨提示：瑞纳冰系列产品形态为冰沙，无法进行少冰去冰操作，请您谅解。建议送达后尽快饮用。到店饮用口感更佳。 ', 'http://newcoffee.wwp666.cn:10006/images/product_small/h001_small.png', 'http://newcoffee.wwp666.cn:10006/images/product_large/h001.png', 1, '冰', '温度', '', '糖', '', '奶', '默认奶油/无奶油', '奶油', '2024-11-18 07:22:51', '2024-11-18 07:22:51');

-- 插入推广内容数据
INSERT INTO promotions (imgUrl, `desc`, sort_order, createdAt, updatedAt) VALUES
('https://ww1.sinaimg.cn/mw690/006b0IMQly1hb1va5egidj333o1y0qjf.jpg', '「瑞幸咖啡 x 线条小狗」情人节限定新品来了！', 1, '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
('https://p3.itc.cn/q_70/images03/20220417/563f3ccba5ea4e1f9e8fd6edd72add84.png', '「瑞幸 x 椰树」 椰云拿铁上线', 2, '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
('https://pic2.zhimg.com/v2-5480a124d868813d32cce87a52dcd609_r.jpg', '民生·luckin coffee 联名信用卡', 3, '2024-11-18 07:22:51', '2024-11-18 07:22:51'),
('https://money.ycwb.com/pic/2020-12/16/90e39574-d151-4362-b556-99b8bc2555b3.jpg', '人气爆款，圣诞节限时55折', 4, '2024-11-18 07:22:51', '2024-11-18 07:22:51');
