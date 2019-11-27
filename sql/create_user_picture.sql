/******************************************/
/*   表名称 = picture   */
/******************************************/
CREATE TABLE IF NOT EXISTS `user_picture` (
  `id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(20) unsigned NOT NULL COMMENT '合照ID',
  `picture_id` int(20) NOT NULL COMMENT '文件名',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modifid_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  foreign key(user_id) references user(id) ON UPDATE CASCADE ON DELETE CASCADE,
  foreign key(picture_id) references picture(id) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT='用户表'
;

