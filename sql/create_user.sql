/******************************************/
/*   表名称 = user   */
/******************************************/
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '',
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT '姓名',
  `password` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '密码',
  `fname` varchar(255) NOT NULL DEFAULT '' COMMENT '文件名',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modifid_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT='用户表'
;
