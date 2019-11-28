/******************************************/
/*   表名称 = picture   */
/******************************************/
CREATE TABLE IF NOT EXISTS `picture` (
  `id` int(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '合照ID',
  `code` varchar(50) NOT NULL DEFAULT '' COMMENT '查看码',
  `fname` varchar(255) NOT NULL DEFAULT '' COMMENT '照片文件名',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modifid_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT='合照表'
;
