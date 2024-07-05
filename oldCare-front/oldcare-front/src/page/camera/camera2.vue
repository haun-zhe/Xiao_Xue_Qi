<template>
    <div class="camera-box">
        <h2 :style="{color:'#959595'}"><b>监控禁区</b></h2>
        <iframe style="border: none" src="http://127.0.0.1:5001/check_fence" width="900" height="500">
        </iframe>
    </div>
</template>
<style>
.camera-box{
    border: none;
    background-color:rgba(177, 173, 173, 0.293);
    height:600px;
    text-align:center;
    padding-top: 10px;
}

</style>
