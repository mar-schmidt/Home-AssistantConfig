#!/bin/bash

xmlgetnext () {
   local IFS='>'
   read -d '<' TAG VALUE
}

cat $1 | while xmlgetnext ; do
   case $TAG in
      'title')
         title="$VALUE"
         ;;
      'category')
         category="$VALUE"
         ((c++)) && ((c==10)) && break
         ;;
      'description')
         description="$VALUE"
         ;;
      '/item')
         cat<<EOF
$category.      $title
                $description
EOF
         ;;
      esac
done
