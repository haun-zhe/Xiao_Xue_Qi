<!-- 情绪识别表 -->
<template>
  <el-table
    :data="emotionData.filter(data => !search || data.oldperson_id.toLowerCase().includes(search.toLowerCase()))"
    style="width: 100%" border>
    <!-- 姓名 -->
    <el-table-column
      align="center"
      fixed
      width="150"
      label="姓名"
      prop="userName">
    </el-table-column>
    <!-- 老人id -->
    <el-table-column
      align="center"
      width="200"
      label="老人id"
      prop="oldperson_id">
    </el-table-column>
    <!-- 地点 -->
    <el-table-column
      align="center"
      width="150"
      label="地点"
      prop="eventLocation">
    </el-table-column>
    <!-- 时间 -->
    <el-table-column
      align="center"
      width="150"
      label="时间"
      prop="eventDate">
    </el-table-column>
    <!-- 情绪 -->
    <el-table-column
      align="center"
      width="150"
      label="情绪"
      prop="eventDesc">
    </el-table-column>
    <!-- 图片 -->
    <el-table-column prop="eventPhoto" label="图片" width="200" align="center">
        <template slot-scope="scope">
            <img :src="scope.row.eventPhoto" style="height: 50px"/>
        </template>
    </el-table-column>
    <!-- 搜索 -->
    <el-table-column
      width="200"
      fixed="right"
      align="right">
      <template slot="header" slot-scope="{}">
        <el-input
          v-model="search"
          size="mini"
          placeholder="请输入老人id搜索"/>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
  export default {
    data() {
      return {
       emotionData : [],
        search: ''
      }
    },
        mounted() {
      this.$axios({
        url:'/table_facial_expression',
        method:'get',
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json;charset=utf-8"
        },
        params: {
          eventType: 0,}
      }).then(res => {
        if(res.status==200){
          if(res.data.code==200){
            this.emotionData =res.data.data
          }else if(res.data.code==-1){
            alert("查询失败！")
          }
        }else{
          alert(res.data.msg)
        }
      })
    },
    methods: {
      handleEdit(index, row) {
        console.log(index, row);
      },
      handleDelete(index, row) {
        console.log(index, row);
      }
    },
  }
</script>