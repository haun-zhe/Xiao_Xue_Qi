<template>
    <div class="face">
        <h2 class="tip"><b>请面向摄像头</b></h2>
        <div class="videos" ref="videos">
            <video id="video_cam" autoplay="autoplay"></video>
            <!-- 移除不必要的 canvas 元素显示 -->
        </div>
        <button @click="back()">返回账号密码登陆</button>
    </div>
</template>

<script>
    export default {
        mounted() {
            this.camera_open().then(() => {
                this.faceRec();
            });
        },
        methods: {
            camera_open() {
                return new Promise((resolve, reject) => {
                    var constraints = {
                        video: {
                            height: 480,
                            width: 640
                        }
                    };
                    let vio = document.getElementById('video_cam');
                    var promise = navigator.mediaDevices.getUserMedia(constraints);
                    promise.then((MediaStream) => {
                        vio.srcObject = MediaStream;
                        vio.play();
                        // 拍照截图，不保存到 this.imgFace
                        setTimeout(() => {
                            let canvas = document.createElement('canvas');
                            canvas.width = 640;
                            canvas.height = 480;
                            canvas.getContext('2d').drawImage(vio, 0, 0, canvas.width, canvas.height);
                            // 发送图像到后端处理
                            this.faceRec(canvas.toDataURL("image/png"));
                            resolve();
                        }, 1000);
                    }).catch((error) => {
                        console.info(error);
                        reject(error);
                    });
                });
            },

            faceRec(imgData) {
                this.$axios({
                    url: 'http://127.0.0.1:5001/face_rec',
                    method: 'post',
                    Credentials: "include",
                    data: {
                        photo: imgData
                    },
                    headers: {
                        "Access-Control-Allow-Origin": "*",
                        "Content-Type": "application/json;charset=utf-8"
                    }
                }).then(res => {
                    if (res.data.code == 200) {
                        alert("登陆成功，欢迎您")
                        this.beforeDestroy();
                        this.$router.push({ path: '/home/first' })
                        location.reload();
                    } else {
                        // alert("人脸登陆失败")
                    }
                }).catch(function (error) {
                    console.log(error)
                })
            },

            back() {
                this.beforeDestroy();
                this.$router.push('/login');
                location.reload();
            },

            beforeDestroy() {
                this.closeVideo();
            },

            closeVideo() {
                this.MediaStreamTrack && this.MediaStreamTrack.stop();
            }
        }
    }
</script>

<style scoped>
    * {
        margin: 0;
        padding: 0;
    }

    .tip {
        margin-top: 5%;
        text-align: center;
    }

    #video_cam {
        height: 480px;
        width: 640px;
        margin-left: 30%;
        margin-top: 5%;
        align-items: center;
        justify-content: center;
        border: solid 1px;
    }

    button {
        color: rgb(89, 88, 88);
        height: 36px;
        width: 160px;
        margin-left: 44.5%;
        margin-top: 25px;
        border: solid 1px;
        border-color: rgb(90, 179, 251);
        border-radius: 8px;
        background: white;
    }

    button:hover {
        background: rgb(90, 179, 251);
        color: white;
    }
</style>
