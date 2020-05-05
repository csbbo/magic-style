<template>
    <div class="style-image">
        <div class="multi-image">
            <div v-for="img in images" :key="img" class="image">
                <div class="img">
                    <img :src="img.now_name">
                    <span class="title">{{img.upload_name}}</span>
                </div>
                <div class="action">
                    <a @click="renameImage(img.id)">重命名</a>
                    <a @click="deleteImage(img.id)">删除</a>
                </div>
            </div>
        </div>

        <form action="#">
            <div class="file-field input-field">
              <div class="btn">
                <span>Go</span>
                <input @change="uploadImage" type="file" multiple accept="image/png,image/gif,image/jpeg">
              </div>
              <div class="file-path-wrapper">
                <input class="file-path validate" type="text" placeholder="上传一张或多张图片">
              </div>
            </div>
            <div v-if="uploadProgress >= 0 && uploadProgress <= 100" class="progress">
              <div class="determinate" :style="{width: uploadProgress + '%'}"></div>
            </div>
        </form>

    </div>
</template>

<script>
    import ajax from 'axios'
    import {GetStyleImage, DeleteStyleImage, UpdateStyleImage} from '../../api'
    export default {
        name: "StyleImage",
        data() {
            return {
                uploadProgress: -1,
                images: [],
            }
        },
        created() {
            this.getImages()
        },
        methods: {
            getImages() {
                GetStyleImage({'image_type': 'for_train'}).then(resp => {
                    if (resp.err === null) {
                        this.images = resp.data
                    }
                })
            },
            async uploadImage(e) {
                this.uploadProgress = -1;
                let files = e.target.files;
                for (let i=0;i<files.length;i++){
                    let param = new FormData();
                    param.append('file',files[i]);
                    console.log(param.get('file'));

                    let headers = {
                      headers:{'Content-Type':'multipart/form-data'}
                    };
                    await ajax.post('/api/UploadStyleImageAPI',param,headers).then(resp => {
                        for (let i=1; i<100; i++) {
                            this.uploadProgress += 1
                        }
                        if (resp.data.err === null) {
                            this.uploadProgress = 100
                        } else {
                            alert(files[i].name+"上传失败")
                            throw "图片上传失败"
                        }
                    })
                }
                this.getImages()
            },
            deleteImage(id) {
                if (!confirm('您确定删除该图片?')) {
                    return
                }
                DeleteStyleImage({'id': id}).then(resp => {
                    if (resp.err === null) {
                        this.getImages()
                    }
                })
            },
            renameImage(id) {
                let update_name = prompt("请输入修改后的风格图片名字");
                if (update_name === null || update_name === '') {
                    return
                }
                UpdateStyleImage({'id': id, 'update_name': update_name}).then(resp => {
                    if (resp.err === null) {
                        this.getImages()
                    }
                })
            }
        }
    }
</script>

<style scoped>
    .multi-image {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }
    .image {
        width: 21%;
        margin: 20px;
        box-shadow: 2px 2px 2px #bdbdbd;
        border-radius: 3px;
    }
    /*.image .title {*/
    /*}*/
    .image img {
        width: 100%;
    }
    .image .action {
        padding: 10px 5px;
        background-color: #FFFFFF;
        border-left: 1px solid #f5f5f5;
    }
    .image .action a{
        margin-right: 10px;
        color: #ffab40;
    }
    .image .action a:hover{
        color: #ffd8a6;
    }

    form {
        margin: 20px;
        width: 30%;
    }
</style>