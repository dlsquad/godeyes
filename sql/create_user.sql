/******************************************/
/*   表名称 = user   */
/******************************************/
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '',
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT '姓名',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modifid_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT='用户表'
;
