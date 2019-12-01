/******************************************/
/*   表名称 = user_picture   */
/******************************************/
CREATE TABLE IF NOT EXISTS `user_picture` (
  `id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(20) unsigned NOT NULL COMMENT '用户ID',
  `picture_id` int(20) unsigned NOT NULL COMMENT '合照ID',
  `pos_x` tinyint(8) NOT NULL COMMENT '第x排，从前到后',
  `pos_y` tinyint(8) NOT NULL COMMENT '第y个，从左到右',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modifid_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  foreign key(user_id) references user(id) ON UPDATE CASCADE ON DELETE CASCADE,
  foreign key(picture_id) references picture(id) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT='合照位置表'
;

