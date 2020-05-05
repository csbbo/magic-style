<template>
  <div class="transfer">
    <div class="content">
      <div class="style-image">
        <div v-for="(img, index) in styleImages" :key="index" class="image">
          <img @click="choiseImg(img.id)" class="selectlist" :src="img.now_name" />
        </div>
      </div>
      <div class="style-select">
        <div class="select-img">
          <div v-for="(img, index) in selectedImages" :key="index" class="select-image">
            <img @click="choiseImg(img.id)" :src="img.now_name" />
          </div>
        </div>
        <div class="translate-btn">
          <a @click="convertImg" class="waves-effect waves-light btn">迁移</a>
        </div>
      </div>
      <div class="img-upload">
        <div class="upload-image">
          <div class="upimage">
            <img :src="originImagePath" />
          </div>
        </div>
        <div class="tool">
          <a class="toolbtn dowload waves-effect waves-light btn">下载</a>

          <div class="toolbtn upload file-field input-field">
            <div class="btn">
              <span>上传</span>
              <input
                @change="uploadImage"
                type="file"
                multiple
                accept="image/png, image/gif, image/jpeg"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ajax from "axios";
import { GetStyleImage, ConvertImage } from "../api";
import { Loading } from "element-ui";
export default {
  name: "Transfer",
  data() {
    return {
      styleImages: [],
      selects: [],
      selectedImages: [],
      originImagePath: "",
      originImageName: ""
    };
  },
  created() {
    this.getImages();
  },
  methods: {
    getImages() {
      GetStyleImage({'image_type': 'trained'}).then(resp => {
        if (resp.err === null) {
          this.styleImages = resp.data;
        }
      });
    },
    choiseImg(id) {
      const index = this.selects.indexOf(id);
      if (index === -1) {
        this.selects.push(id);
      } else {
        this.selects.splice(index, 1);
      }

      this.selectedImages = [];
      for (let i = 0; i < this.styleImages.length; i++) {
        const item = this.selects.indexOf(this.styleImages[i].id);
        if (item !== -1) {
          this.selectedImages.push(this.styleImages[i]);
        }
      }
    },
    uploadImage(e) {
      const loading = this.$loading({
        lock: true,
        text: "正在上传。。。",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
        target: document.querySelector(".upload-image")
      });
      let file = e.target.files[0];
      let param = new FormData();
      param.append("file", file);
      console.log(param.get("file"));

      let headers = {
        headers: { "Content-Type": "multipart/form-data" }
      };
      ajax.post("/api/UploadImageAPI", param, headers).then(resp => {
        if (resp.data.err === null) {
          loading.close();
          this.originImagePath = resp.data.data.origin_image_path;
          this.originImageName = resp.data.data.name;
        }
      });
    },
    convertImg() {
      const loading = this.$loading({
        lock: true,
        text: "正在渲染。。。",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
        target: document.querySelector(".upload-image")
      });
      let style_list = [];
      for (let i = 0; i < this.selectedImages.length; i++) {
        style_list.push(this.selectedImages[i].id);
      }
      const data = {
        origin_image: this.originImageName,
        style_images: style_list
      };
      ConvertImage(data).then(resp => {
        loading.close();
        this.originImagePath = resp.data.generate_image;
      });
    }
  }
};
</script>

<style scoped>
.content {
  display: flex;
  justify-content: space-between;
  padding: 20px 10px;
}

.style-image {
  display: flex;
  flex-direction: row;
  width: 50%;
  border: 2px solid #bbdefb;
  border-radius: 10px 0px 0px 10px;
  padding: 5px;
  flex-wrap: wrap;
}
.style-select {
  width: 10%;
  display: flex;
  flex-direction: column;
}

.style-select .select-img {
  border: 2px solid #bbdefb;
  height: 800px;
  overflow-x: hidden;
  overflow-y: scroll;
  flex-wrap: wrap;
}
.style-select .select-img::-webkit-scrollbar {
  display: none;
}
.img-upload {
  width: 38%;
  display: flex;
  flex-direction: column;
  border: 2px solid #bbdefb;
  border-radius: 0px 10px 10px 0px;
}

.image {
  width: 150px;
  margin: 5px;
  padding: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #009688;
}
.image img {
  width: 100%;
  border: 2px solid #009688;
  padding: 2px;
}
.translate-btn {
  height: 40px;
  margin-top: 5px;
}
.translate-btn .btn {
  width: 100%;
  border-radius: 6px;
  font-size: 20px;
  background-color: #ff8f00;
}
.select-image {
  width: 90%;
  margin: 7px;
}
.select-image img {
  width: 100%;
  margin: 5px;
  padding: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #009688;
}

.img-upload .upload-image {
  width: 90%;
  margin: 20px auto;
  height: 90%;
}
.img-upload .upload-image img {
  width: 90%;
  margin: 20px;
}
.img-upload .tool {
  width: 90%;
  margin: 25px auto;
  height: 30px;
  border-top: 2px solid #c5cae9;
  padding-top: 5px;
}
.img-upload .tool .toolbtn {
  float: right;
  margin-left: 10px;
}
.img-upload .tool .upload {
  margin: 0;
}
.img-upload .tool .dowload {
  height: 44px;
  padding-top: 4px;
}
.image .selectlist {
  border-color: #ffffff;
}
</style>