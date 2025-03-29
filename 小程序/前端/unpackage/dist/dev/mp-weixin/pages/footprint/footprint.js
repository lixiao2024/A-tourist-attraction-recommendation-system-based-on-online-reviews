(global["webpackJsonp"] = global["webpackJsonp"] || []).push([["pages/footprint/footprint"],{

/***/ 118:
/*!************************************************************************************!*\
  !*** I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/main.js?{"page":"pages%2Ffootprint%2Ffootprint"} ***!
  \************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(wx, createPage) {

var _interopRequireDefault = __webpack_require__(/*! @babel/runtime/helpers/interopRequireDefault */ 4);
__webpack_require__(/*! uni-pages */ 26);
__webpack_require__(/*! @dcloudio/vue-cli-plugin-uni/packages/uni-cloud/dist/index.js */ 27);
var _vue = _interopRequireDefault(__webpack_require__(/*! vue */ 25));
var _footprint = _interopRequireDefault(__webpack_require__(/*! ./pages/footprint/footprint.vue */ 119));
// @ts-ignore
wx.__webpack_require_UNI_MP_PLUGIN__ = __webpack_require__;
createPage(_footprint.default);
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./node_modules/@dcloudio/uni-mp-weixin/dist/wx.js */ 1)["default"], __webpack_require__(/*! ./node_modules/@dcloudio/uni-mp-weixin/dist/index.js */ 2)["createPage"]))

/***/ }),

/***/ 119:
/*!*****************************************************************!*\
  !*** I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/footprint/footprint.vue ***!
  \*****************************************************************/
/*! no static exports found */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _footprint_vue_vue_type_template_id_60cb6cf4___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./footprint.vue?vue&type=template&id=60cb6cf4& */ 120);
/* harmony import */ var _footprint_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./footprint.vue?vue&type=script&lang=js& */ 122);
/* harmony reexport (unknown) */ for(var __WEBPACK_IMPORT_KEY__ in _footprint_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__) if(["default"].indexOf(__WEBPACK_IMPORT_KEY__) < 0) (function(key) { __webpack_require__.d(__webpack_exports__, key, function() { return _footprint_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__[key]; }) }(__WEBPACK_IMPORT_KEY__));
/* harmony import */ var _footprint_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./footprint.vue?vue&type=style&index=0&lang=scss& */ 129);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/runtime/componentNormalizer.js */ 44);

var renderjs





/* normalize component */

var component = Object(_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__["default"])(
  _footprint_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _footprint_vue_vue_type_template_id_60cb6cf4___WEBPACK_IMPORTED_MODULE_0__["render"],
  _footprint_vue_vue_type_template_id_60cb6cf4___WEBPACK_IMPORTED_MODULE_0__["staticRenderFns"],
  false,
  null,
  null,
  null,
  false,
  _footprint_vue_vue_type_template_id_60cb6cf4___WEBPACK_IMPORTED_MODULE_0__["components"],
  renderjs
)

component.options.__file = "pages/footprint/footprint.vue"
/* harmony default export */ __webpack_exports__["default"] = (component.exports);

/***/ }),

/***/ 120:
/*!************************************************************************************************!*\
  !*** I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/footprint/footprint.vue?vue&type=template&id=60cb6cf4& ***!
  \************************************************************************************************/
/*! exports provided: render, staticRenderFns, recyclableRender, components */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_17_0_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_template_id_60cb6cf4___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--17-0!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/webpack-uni-mp-loader/lib/template.js!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-uni-app-loader/page-meta.js!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!./footprint.vue?vue&type=template&id=60cb6cf4& */ 121);
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "render", function() { return _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_17_0_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_template_id_60cb6cf4___WEBPACK_IMPORTED_MODULE_0__["render"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "staticRenderFns", function() { return _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_17_0_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_template_id_60cb6cf4___WEBPACK_IMPORTED_MODULE_0__["staticRenderFns"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "recyclableRender", function() { return _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_17_0_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_template_id_60cb6cf4___WEBPACK_IMPORTED_MODULE_0__["recyclableRender"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "components", function() { return _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_17_0_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_template_id_60cb6cf4___WEBPACK_IMPORTED_MODULE_0__["components"]; });



/***/ }),

/***/ 121:
/*!************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--17-0!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/template.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-uni-app-loader/page-meta.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/footprint/footprint.vue?vue&type=template&id=60cb6cf4& ***!
  \************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/*! exports provided: render, staticRenderFns, recyclableRender, components */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "render", function() { return render; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "staticRenderFns", function() { return staticRenderFns; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "recyclableRender", function() { return recyclableRender; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "components", function() { return components; });
var components
try {
  components = {
    uniIcons: function () {
      return Promise.all(/*! import() | uni_modules/uni-icons/components/uni-icons/uni-icons */[__webpack_require__.e("common/vendor"), __webpack_require__.e("uni_modules/uni-icons/components/uni-icons/uni-icons")]).then(__webpack_require__.bind(null, /*! @/uni_modules/uni-icons/components/uni-icons/uni-icons.vue */ 131))
    },
  }
} catch (e) {
  if (
    e.message.indexOf("Cannot find module") !== -1 &&
    e.message.indexOf(".vue") !== -1
  ) {
    console.error(e.message)
    console.error("1. 排查组件名称拼写是否正确")
    console.error(
      "2. 排查组件是否符合 easycom 规范，文档：https://uniapp.dcloud.net.cn/collocation/pages?id=easycom"
    )
    console.error(
      "3. 若组件不符合 easycom 规范，需手动引入，并在 components 中注册该组件"
    )
  } else {
    throw e
  }
}
var render = function () {
  var _vm = this
  var _h = _vm.$createElement
  var _c = _vm._self._c || _h
}
var recyclableRender = false
var staticRenderFns = []
render._withStripped = true



/***/ }),

/***/ 122:
/*!******************************************************************************************!*\
  !*** I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/footprint/footprint.vue?vue&type=script&lang=js& ***!
  \******************************************************************************************/
/*! no static exports found */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/babel-loader/lib!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--13-1!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/webpack-uni-mp-loader/lib/script.js!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!./footprint.vue?vue&type=script&lang=js& */ 123);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__);
/* harmony reexport (unknown) */ for(var __WEBPACK_IMPORT_KEY__ in _HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__) if(["default"].indexOf(__WEBPACK_IMPORT_KEY__) < 0) (function(key) { __webpack_require__.d(__webpack_exports__, key, function() { return _HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__[key]; }) }(__WEBPACK_IMPORT_KEY__));
 /* harmony default export */ __webpack_exports__["default"] = (_HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0___default.a); 

/***/ }),

/***/ 123:
/*!*************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--13-1!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/script.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/footprint/footprint.vue?vue&type=script&lang=js& ***!
  \*************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(uni, wx) {

var _typeof = __webpack_require__(/*! @babel/runtime/helpers/typeof */ 13);
Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;
var echarts = _interopRequireWildcard(__webpack_require__(/*! @/js/echarts.js */ 124));
function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function _getRequireWildcardCache(nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }
function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || _typeof(obj) !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//

// 修改 echarts 导入方式

// 不再使用import导入china.js，而是在方法中动态加载

// 内置地图数据 - 简化版中国地图数据（精简版，实际使用时可以替换为完整版）
var simpleChinaGeoJSON = {
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "properties": {
      "name": "北京"
    },
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[116.1, 40.1], [116.1, 39.7], [116.7, 39.7], [116.7, 40.1], [116.1, 40.1]]]
    }
  }, {
    "type": "Feature",
    "properties": {
      "name": "上海"
    },
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[121.1, 31.5], [121.1, 30.9], [121.8, 30.9], [121.8, 31.5], [121.1, 31.5]]]
    }
  }, {
    "type": "Feature",
    "properties": {
      "name": "广州"
    },
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[113.0, 23.4], [113.0, 22.8], [113.6, 22.8], [113.6, 23.4], [113.0, 23.4]]]
    }
  }, {
    "type": "Feature",
    "properties": {
      "name": "深圳"
    },
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[113.7, 22.8], [113.7, 22.4], [114.4, 22.4], [114.4, 22.8], [113.7, 22.8]]]
    }
  }, {
    "type": "Feature",
    "properties": {
      "name": "南京"
    },
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[118.5, 32.3], [118.5, 31.9], [119.0, 31.9], [119.0, 32.3], [118.5, 32.3]]]
    }
  }]
};

// 简化版世界地图（仅包含中国）
var simpleWorldGeoJSON = {
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "properties": {
      "name": "中国"
    },
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[73, 53], [73, 18], [135, 18], [135, 53], [73, 53]]]
    }
  }]
};

// 地图数据
var chinaJson = null;
var worldJson = null;
var _default = {
  data: function data() {
    return {
      chinaMap: null,
      visitedCities: [{
        name: '北京',
        value: 1
      }, {
        name: '上海',
        value: 1
      }, {
        name: '广州',
        value: 1
      }],
      // 添加足迹数据对象
      footprintData: {
        cities: {
          '北京': {
            visitCount: 1,
            firstVisit: '2023-01-01'
          },
          '上海': {
            visitCount: 1,
            firstVisit: '2023-02-15'
          },
          '广州': {
            visitCount: 1,
            firstVisit: '2023-03-20'
          }
        }
      },
      // 城市坐标数据
      cityCoordinates: {},
      // 添加统计信息
      stats: {
        visitedCount: 0,
        chinaRate: '0%'
      },
      // 地图数据加载状态
      mapLoadingFailed: false,
      isLoading: false
    };
  },
  // 页面加载完成后初始化
  onLoad: function onLoad() {
    // 从本地存储加载足迹数据
    var savedData = uni.getStorageSync('footprint_data');
    if (savedData) {
      try {
        this.footprintData = JSON.parse(savedData);
        // 更新访问城市列表
        this.updateVisitedCities();
      } catch (e) {
        console.error('解析足迹数据失败:', e);
      }
    }
  },
  // 页面显示时初始化地图
  onReady: function onReady() {
    this.initMapData();
  },
  methods: {
    // 添加新的方法来读取本地文件
    readLocalChinaJs: function readLocalChinaJs() {
      return new Promise(function (resolve, reject) {
        // 在小程序环境下，尝试读取本地文件
        var fsm = uni.getFileSystemManager();

        // 尝试各种可能的路径
        var paths = ["".concat(wx.env.USER_DATA_PATH, "/china.js"), 'static/map/china.js', '/static/map/china.js', 'I:/基于在线评论的旅游景点智能推荐系统/前端/static/map/china.js' // 尝试直接使用绝对路径
        ];

        // 函数化读取尝试
        var tryReadFile = function tryReadFile(index) {
          if (index >= paths.length) {
            // 所有路径都失败了，尝试通过网络请求获取
            uni.request({
              url: 'https://echarts.apache.org/examples/vendors/echarts/map/js/china.js',
              success: function success(res) {
                if (res.data) {
                  console.log('通过CDN获取地图数据成功');
                  resolve(res.data);
                } else {
                  reject(new Error('CDN地图数据为空'));
                }
              },
              fail: function fail(err) {
                console.error('通过CDN获取地图数据失败:', err);
                reject(err);
              }
            });
            return;
          }

          // 尝试读取当前路径
          fsm.readFile({
            filePath: paths[index],
            encoding: 'utf-8',
            success: function success(res) {
              console.log("\u6210\u529F\u4ECE\u8DEF\u5F84 ".concat(paths[index], " \u8BFB\u53D6\u5730\u56FE\u6570\u636E"));
              resolve(res.data);
            },
            fail: function fail(err) {
              console.error("\u4ECE\u8DEF\u5F84 ".concat(paths[index], " \u8BFB\u53D6\u5931\u8D25:"), err);
              // 尝试下一个路径
              tryReadFile(index + 1);
            }
          });
        };

        // 开始尝试第一个路径
        tryReadFile(0);
      });
    },
    // 初始化地图数据
    initMapData: function initMapData() {
      var _this = this;
      try {
        this.isLoading = true;
        uni.showLoading({
          title: '初始化地图...'
        });

        // 首先尝试读取本地文件
        this.readLocalChinaJs().then(function (data) {
          try {
            // 执行获取的JS代码
            eval(data);
            console.log('成功加载本地地图数据');
          } catch (e) {
            console.error('执行地图数据失败:', e);
          }

          // 无论成功与否，都继续初始化
          setTimeout(function () {
            _this.initChinaMap();
            _this.updateStats();
            _this.isLoading = false;
            uni.hideLoading();
          }, 500);
        }).catch(function (err) {
          console.error('读取本地文件失败，尝试网络请求:', err);

          // 退回到网络请求方式
          uni.request({
            url: '/static/map/china.js',
            success: function success(res) {
              console.log('成功加载网络地图数据');
              try {
                if (res.data) {
                  eval(res.data);
                }
              } catch (e) {
                console.error('执行网络地图数据失败:', e);
              }
              setTimeout(function () {
                _this.initChinaMap();
                _this.updateStats();
                _this.isLoading = false;
                uni.hideLoading();
              }, 500);
            },
            fail: function fail() {
              console.log('所有加载方式均失败，使用内置数据');
              setTimeout(function () {
                _this.initChinaMap();
                _this.updateStats();
                _this.isLoading = false;
                uni.hideLoading();
              }, 500);
            }
          });
        });
      } catch (error) {
        this.isLoading = false;
        uni.hideLoading();
        console.error('地图初始化失败:', error);
        this.mapLoadingFailed = true;
        uni.showToast({
          title: '地图初始化失败',
          icon: 'none'
        });
      }
    },
    // 初始化中国地图 - 使用新的方式来处理微信小程序的ECharts
    initChinaMap: function initChinaMap() {
      var _this2 = this;
      var query = uni.createSelectorQuery().in(this);
      query.select('#chinaMap').fields({
        node: true,
        size: true
      }).exec(function (res) {
        if (res[0] && res[0].node) {
          var canvas = res[0].node;
          var ctx = canvas.getContext('2d');

          // 设置canvas尺寸，适应高分辨率
          var dpr = uni.getSystemInfoSync().pixelRatio;
          canvas.width = res[0].width * dpr;
          canvas.height = res[0].height * dpr;
          try {
            // 手动注册中国地图数据
            if (!echarts.getMap('china')) {
              console.log('开始注册地图...');

              // 尝试获取被正确加载的地图数据
              if (window && window.echarts && window.echarts.registerMap) {
                console.log('检测到window.echarts，尝试获取已注册地图');
                // 如果在window对象上有echarts，可能已经注册了地图
              } else {
                console.log('使用内置简化版地图数据');
                // 使用内置的简化版中国地图数据
                var chinaMapData = {
                  "type": "FeatureCollection",
                  "features": [{
                    "type": "Feature",
                    "id": "110000",
                    "properties": {
                      "id": "110000",
                      "cp": [116.405285, 39.904989],
                      "name": "北京",
                      "childNum": 1
                    },
                    "geometry": {
                      "type": "Polygon",
                      "coordinates": [[[116.1, 40.1], [116.1, 39.7], [116.7, 39.7], [116.7, 40.1], [116.1, 40.1]]]
                    }
                  }, {
                    "type": "Feature",
                    "id": "310000",
                    "properties": {
                      "id": "310000",
                      "cp": [121.472644, 31.231706],
                      "name": "上海",
                      "childNum": 1
                    },
                    "geometry": {
                      "type": "Polygon",
                      "coordinates": [[[121.1, 31.5], [121.1, 30.9], [121.8, 30.9], [121.8, 31.5], [121.1, 31.5]]]
                    }
                  }, {
                    "type": "Feature",
                    "id": "440100",
                    "properties": {
                      "id": "440100",
                      "cp": [113.280637, 23.125178],
                      "name": "广州",
                      "childNum": 1
                    },
                    "geometry": {
                      "type": "Polygon",
                      "coordinates": [[[113.0, 23.4], [113.0, 22.8], [113.6, 22.8], [113.6, 23.4], [113.0, 23.4]]]
                    }
                  }, {
                    "type": "Feature",
                    "id": "440300",
                    "properties": {
                      "id": "440300",
                      "cp": [114.085947, 22.547],
                      "name": "深圳",
                      "childNum": 1
                    },
                    "geometry": {
                      "type": "Polygon",
                      "coordinates": [[[113.7, 22.8], [113.7, 22.4], [114.4, 22.4], [114.4, 22.8], [113.7, 22.8]]]
                    }
                  }, {
                    "type": "Feature",
                    "id": "320100",
                    "properties": {
                      "id": "320100",
                      "cp": [118.767413, 32.041544],
                      "name": "南京",
                      "childNum": 1
                    },
                    "geometry": {
                      "type": "Polygon",
                      "coordinates": [[[118.5, 32.3], [118.5, 31.9], [119.0, 31.9], [119.0, 32.3], [118.5, 32.3]]]
                    }
                  }, {
                    "type": "Feature",
                    "id": "330100",
                    "properties": {
                      "id": "330100",
                      "cp": [120.153576, 30.287459],
                      "name": "杭州",
                      "childNum": 1
                    },
                    "geometry": {
                      "type": "Polygon",
                      "coordinates": [[[120.0, 30.5], [120.0, 30.0], [120.5, 30.0], [120.5, 30.5], [120.0, 30.5]]]
                    }
                  }, {
                    "type": "Feature",
                    "id": "510100",
                    "properties": {
                      "id": "510100",
                      "cp": [104.065735, 30.659462],
                      "name": "成都",
                      "childNum": 1
                    },
                    "geometry": {
                      "type": "Polygon",
                      "coordinates": [[[103.8, 30.9], [103.8, 30.4], [104.3, 30.4], [104.3, 30.9], [103.8, 30.9]]]
                    }
                  }]
                };
                echarts.registerMap('china', chinaMapData);
                console.log('已手动注册中国地图数据');
              }

              // 小程序特殊处理：模拟DOM元素的关键属性和方法
              var canvasNode = {
                nodeType: 1,
                // 元素节点
                tagName: 'canvas',
                width: canvas.width,
                height: canvas.height,
                ctx: ctx,
                style: {},
                getBoundingClientRect: function getBoundingClientRect() {
                  return {
                    width: res[0].width,
                    height: res[0].height
                  };
                },
                createSVGRect: function createSVGRect() {},
                setAttribute: function setAttribute() {},
                getContext: function getContext(type) {
                  if (type === '2d') return ctx;
                  return null;
                },
                // 添加事件监听器模拟方法
                addEventListener: function addEventListener(type, listener, options) {
                  // 在小程序环境中，事件监听不能直接添加，所以这里只是一个空函数
                  console.log('模拟addEventListener:', type);
                  // 存储事件以便将来可能的处理
                  if (!this._eventListeners) this._eventListeners = {};
                  if (!this._eventListeners[type]) this._eventListeners[type] = [];
                  this._eventListeners[type].push({
                    listener: listener,
                    options: options
                  });
                },
                // 移除事件监听器模拟方法
                removeEventListener: function removeEventListener(type, listener, options) {
                  console.log('模拟removeEventListener:', type);
                  // 同样是空实现
                  if (!this._eventListeners || !this._eventListeners[type]) return;
                  this._eventListeners[type] = this._eventListeners[type].filter(function (item) {
                    return item.listener !== listener;
                  });
                },
                // 其他可能需要的方法
                dispatchEvent: function dispatchEvent(event) {
                  console.log('模拟dispatchEvent:', event.type);
                  return true;
                }
              };
              _this2.chinaMap = echarts.init(canvasNode, null, {
                width: res[0].width,
                height: res[0].height,
                devicePixelRatio: dpr,
                renderer: 'canvas',
                useDirtyRect: false
              });

              // 配置中国地图
              var option = {
                title: {
                  text: '我的旅行足迹',
                  subtext: '点击下方按钮添加位置',
                  left: 'center'
                },
                tooltip: {
                  show: false
                },
                visualMap: {
                  min: 0,
                  max: 10,
                  // 设置一个合理的最大值
                  left: 'left',
                  top: 'bottom',
                  text: ['高', '低'],
                  calculable: false,
                  inRange: {
                    color: ['#C0C0C0', '#FFD700'] // 灰色到金色
                  }
                },

                series: [{
                  name: '足迹',
                  type: 'map',
                  map: 'china',
                  roam: false,
                  // 禁用缩放和平移
                  silent: true,
                  // 禁用鼠标事件
                  emphasis: {
                    disabled: true // 禁用高亮效果
                  },

                  data: _this2.visitedCities
                }]
              };

              // 设置option
              _this2.chinaMap.setOption(option);

              // 为小程序环境添加自定义渲染函数
              if (_this2.chinaMap._zr && _this2.chinaMap._zr.painter) {
                var oldRefresh = _this2.chinaMap._zr.painter.refresh;
                _this2.chinaMap._zr.painter.refresh = function () {
                  console.log('自定义渲染处理');
                  // 手动调用原始的渲染方法或进行简化渲染
                  if (typeof oldRefresh === 'function') {
                    try {
                      oldRefresh.apply(this, arguments);
                    } catch (e) {
                      console.error('渲染时发生错误:', e);
                    }
                  }

                  // 确保画布内容显示
                  if (ctx.draw) {
                    ctx.draw(true);
                  }
                };
              }

              // 触发一次渲染
              setTimeout(function () {
                try {
                  if (_this2.chinaMap._zr && _this2.chinaMap._zr.painter) {
                    _this2.chinaMap._zr.painter.refresh();
                  }
                } catch (e) {
                  console.error('手动刷新出错:', e);
                }
              }, 200);
              console.log('中国地图初始化成功');
            }
          } catch (error) {
            console.error('中国地图初始化失败:', error);

            // 如果ECharts初始化失败，使用备用的Canvas绘制方式
            _this2.drawSimpleChina(ctx, canvas.width, canvas.height, dpr);
          }
        } else {
          console.error('获取Canvas节点失败');
        }
      });
    },
    // 备用方案：简单绘制中国地图
    drawSimpleChina: function drawSimpleChina(ctx, width, height, dpr) {
      // 清空画布
      ctx.clearRect(0, 0, width, height);

      // 缩放以适应高分辨率
      ctx.scale(dpr, dpr);

      // 设置背景色
      ctx.fillStyle = "#f8f9fa";
      ctx.fillRect(0, 0, width / dpr, height / dpr);

      // 绘制标题
      ctx.fillStyle = "#333";
      ctx.font = "bold 24px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("我的旅行足迹", width / (2 * dpr), 40);

      // 简化的中国地图轮廓
      this.drawSimplifiedChina(ctx, width / dpr, height / dpr);

      // 在地图上标记已访问的城市
      this.markCities(ctx, width / dpr, height / dpr);

      // 绘制足迹列表
      this.drawCityList(ctx, width / dpr, height / dpr);

      // 恢复缩放
      ctx.scale(1 / dpr, 1 / dpr);
    },
    // 绘制简化的中国地图
    drawSimplifiedChina: function drawSimplifiedChina(ctx, width, height) {
      // 设置绘图样式
      ctx.strokeStyle = "#ccc";
      ctx.lineWidth = 1;
      ctx.fillStyle = "#e6e6e6";

      // 简化的地图轮廓 - 使用大致的中国轮廓
      var mapWidth = width * 0.8;
      var mapHeight = height * 0.5;
      var mapX = (width - mapWidth) / 2;
      var mapY = height * 0.2;

      // 绘制大致轮廓
      ctx.beginPath();
      ctx.moveTo(mapX + mapWidth * 0.2, mapY + mapHeight * 0.2); // 西北角
      ctx.lineTo(mapX + mapWidth * 0.8, mapY + mapHeight * 0.1); // 东北角
      ctx.lineTo(mapX + mapWidth * 0.9, mapY + mapHeight * 0.5); // 东边中部
      ctx.lineTo(mapX + mapWidth * 0.8, mapY + mapHeight * 0.9); // 东南角
      ctx.lineTo(mapX + mapWidth * 0.5, mapY + mapHeight * 0.9); // 南边中部
      ctx.lineTo(mapX + mapWidth * 0.3, mapY + mapHeight * 0.8); // 西南角
      ctx.lineTo(mapX + mapWidth * 0.1, mapY + mapHeight * 0.6); // 西边
      ctx.lineTo(mapX + mapWidth * 0.1, mapY + mapHeight * 0.3); // 西北部
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // 绘制主要区域标签
      ctx.fillStyle = "#666";
      ctx.font = "12px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("东北", mapX + mapWidth * 0.7, mapY + mapHeight * 0.2);
      ctx.fillText("华北", mapX + mapWidth * 0.5, mapY + mapHeight * 0.3);
      ctx.fillText("华东", mapX + mapWidth * 0.8, mapY + mapHeight * 0.5);
      ctx.fillText("中南", mapX + mapWidth * 0.6, mapY + mapHeight * 0.7);
      ctx.fillText("西南", mapX + mapWidth * 0.3, mapY + mapHeight * 0.7);
      ctx.fillText("西北", mapX + mapWidth * 0.3, mapY + mapHeight * 0.3);
    },
    // 在地图上标记城市
    markCities: function markCities(ctx, width, height) {
      var mapWidth = width * 0.8;
      var mapHeight = height * 0.5;
      var mapX = (width - mapWidth) / 2;
      var mapY = height * 0.2;

      // 城市位置映射（简化为大致区域）
      var cityPositions = {
        '北京': [mapX + mapWidth * 0.55, mapY + mapHeight * 0.25],
        '上海': [mapX + mapWidth * 0.8, mapY + mapHeight * 0.5],
        '广州': [mapX + mapWidth * 0.65, mapY + mapHeight * 0.8],
        '深圳': [mapX + mapWidth * 0.67, mapY + mapHeight * 0.85],
        '南京': [mapX + mapWidth * 0.7, mapY + mapHeight * 0.45],
        '杭州': [mapX + mapWidth * 0.75, mapY + mapHeight * 0.55],
        '成都': [mapX + mapWidth * 0.35, mapY + mapHeight * 0.65],
        '重庆': [mapX + mapWidth * 0.42, mapY + mapHeight * 0.68],
        '西安': [mapX + mapWidth * 0.45, mapY + mapHeight * 0.45],
        '武汉': [mapX + mapWidth * 0.58, mapY + mapHeight * 0.55],
        '长沙': [mapX + mapWidth * 0.53, mapY + mapHeight * 0.65],
        '郑州': [mapX + mapWidth * 0.52, mapY + mapHeight * 0.4],
        '哈尔滨': [mapX + mapWidth * 0.7, mapY + mapHeight * 0.1],
        '沈阳': [mapX + mapWidth * 0.65, mapY + mapHeight * 0.2],
        '天津': [mapX + mapWidth * 0.57, mapY + mapHeight * 0.3],
        '青岛': [mapX + mapWidth * 0.65, mapY + mapHeight * 0.4],
        '厦门': [mapX + mapWidth * 0.7, mapY + mapHeight * 0.7]
      };

      // 标记已访问的城市
      ctx.fillStyle = "#FFD700"; // 金色标记
      ctx.strokeStyle = "#333";
      ctx.lineWidth = 0.5;
      this.visitedCities.forEach(function (city) {
        var position = cityPositions[city.name];
        if (position) {
          // 绘制圆点
          ctx.beginPath();
          ctx.arc(position[0], position[1], 6, 0, Math.PI * 2);
          ctx.fill();
          ctx.stroke();

          // 绘制城市名
          ctx.fillStyle = "#333";
          ctx.font = "10px sans-serif";
          ctx.textAlign = "center";
          ctx.fillText(city.name, position[0], position[1] - 10);

          // 恢复标记颜色
          ctx.fillStyle = "#FFD700";
        }
      });
    },
    // 绘制城市列表
    drawCityList: function drawCityList(ctx, width, height) {
      var mapHeight = height * 0.5;
      var mapY = height * 0.2;

      // 绘制已访问城市列表标题
      ctx.fillStyle = "#333";
      ctx.font = "14px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("已访问城市", width / 2, mapY + mapHeight + 30);

      // 城市名称列表
      var cityNames = this.visitedCities.map(function (city) {
        return city.name;
      }).join('、');

      // 绘制城市名称列表（带换行）
      ctx.font = "12px sans-serif";
      ctx.textAlign = "center";

      // 自动换行
      this.wrapText(ctx, cityNames, width / 2, mapY + mapHeight + 50, width * 0.9, 18);

      // 覆盖率信息
      ctx.textAlign = "center";
      ctx.fillText("\u60A8\u5DF2\u63A2\u7D22\u4E86\u4E2D\u56FD".concat(this.stats.chinaRate, "\u7684\u57CE\u5E02"), width / 2, height - 30);
    },
    // 文本自动换行绘制函数
    wrapText: function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
      if (!text) return y;

      // 处理参数
      maxWidth = maxWidth || 100;
      lineHeight = lineHeight || 20;

      // 中文分词按字符分割
      var characters = text.split('');
      var line = '';
      var newY = y;
      for (var i = 0; i < characters.length; i++) {
        var testLine = line + characters[i];
        var metrics = ctx.measureText(testLine);
        var testWidth = metrics.width;
        if (testWidth > maxWidth && i > 0) {
          ctx.fillText(line, x, newY);
          line = characters[i];
          newY += lineHeight;
        } else {
          line = testLine;
        }
      }

      // 绘制最后一行
      ctx.fillText(line, x, newY);
      return newY + lineHeight;
    },
    // 获取用户当前位置并添加到足迹
    getUserLocation: function getUserLocation() {
      var _this3 = this;
      if (this.isLoading) return;
      this.isLoading = true;
      uni.showLoading({
        title: '获取位置信息...'
      });

      // 使用getFuzzyLocation获取模糊位置，因为小程序只申请了模糊地址接口
      uni.getFuzzyLocation({
        type: 'wgs84',
        success: function success(res) {
          uni.hideLoading();
          console.log('获取模糊位置成功:', res);

          // 经纬度反向解析为地址
          _this3.getAddressFromLocation(res.latitude, res.longitude);
        },
        fail: function fail(err) {
          _this3.isLoading = false;
          uni.hideLoading();
          console.error('获取位置失败:', err);
          // 如果获取位置失败，允许用户手动输入
          _this3.showManualInputDialog();
        }
      });
    },
    // 使用经纬度反向解析地址
    getAddressFromLocation: function getAddressFromLocation(latitude, longitude) {
      var _this4 = this;
      uni.showLoading({
        title: '解析位置信息...'
      });

      // 使用腾讯地图API反向解析
      uni.request({
        url: "https://apis.map.qq.com/ws/geocoder/v1/?key=KNLBZ-GNUKT-L6DXC-VRGBS-5G3IF-TVBN7&location=".concat(latitude, ",").concat(longitude),
        success: function success(res) {
          _this4.isLoading = false;
          uni.hideLoading();
          if (res.statusCode === 200 && res.data && res.data.result) {
            // 获取城市名称
            var cityName = res.data.result.address_component.city;
            if (cityName) {
              // 提示用户确认
              uni.showModal({
                title: '添加足迹',
                content: "\u68C0\u6D4B\u5230\u60A8\u5F53\u524D\u4F4D\u4E8E ".concat(cityName, "\uFF0C\u662F\u5426\u6DFB\u52A0\u5230\u8DB3\u8FF9\uFF1F"),
                success: function success(modalRes) {
                  if (modalRes.confirm) {
                    _this4.addVisitedCity(cityName);
                    uni.showToast({
                      title: "\u5DF2\u6DFB\u52A0".concat(cityName, "\u5230\u8DB3\u8FF9"),
                      icon: 'success'
                    });
                  }
                }
              });
            } else {
              _this4.showManualInputDialog();
            }
          } else {
            console.error('地址解析失败:', res);
            _this4.showManualInputDialog();
          }
        },
        fail: function fail(err) {
          _this4.isLoading = false;
          uni.hideLoading();
          console.error('地址解析请求失败:', err);
          _this4.showManualInputDialog();
        }
      });
    },
    // 显示手动输入对话框
    showManualInputDialog: function showManualInputDialog() {
      var _this5 = this;
      uni.showModal({
        title: '添加足迹',
        content: '无法自动获取位置，请手动输入您想要添加的城市名称',
        editable: true,
        placeholderText: '例如：北京',
        success: function success(modalRes) {
          if (modalRes.confirm && modalRes.content) {
            var cityName = modalRes.content;
            _this5.addVisitedCity(cityName);
            uni.showToast({
              title: "\u5DF2\u6DFB\u52A0".concat(cityName, "\u5230\u8DB3\u8FF9"),
              icon: 'success'
            });
          }
        }
      });
    },
    // 添加已访问城市
    addVisitedCity: function addVisitedCity(cityName) {
      if (!cityName) return;

      // 去掉可能存在的"市"字
      var cleanCityName = cityName.replace('市', '');

      // 检查是否已经存在该城市
      if (this.footprintData.cities[cleanCityName]) {
        // 已存在，增加访问次数
        this.footprintData.cities[cleanCityName].visitCount++;

        // 更新对应城市的value值
        var cityIndex = this.visitedCities.findIndex(function (city) {
          return city.name === cleanCityName;
        });
        if (cityIndex !== -1) {
          this.visitedCities[cityIndex].value = this.footprintData.cities[cleanCityName].visitCount;
        }
      } else {
        // 新城市，添加记录
        this.footprintData.cities[cleanCityName] = {
          visitCount: 1,
          firstVisit: new Date().toISOString().split('T')[0]
        };

        // 添加到访问城市列表
        this.visitedCities.push({
          name: cleanCityName,
          value: 1
        });
      }

      // 保存数据并刷新地图
      this.saveFootprintData();
      this.refreshMap();
    },
    // 保存足迹数据
    saveFootprintData: function saveFootprintData() {
      try {
        // 将数据保存到本地存储
        uni.setStorageSync('footprint_data', JSON.stringify(this.footprintData));
      } catch (e) {
        console.error('保存足迹数据失败:', e);
      }
    },
    // 刷新地图
    refreshMap: function refreshMap() {
      // 更新统计信息
      this.updateStats();

      // 如果echarts实例存在，更新数据
      if (this.chinaMap) {
        this.chinaMap.setOption({
          series: [{
            data: this.visitedCities
          }]
        });
      } else {
        // 否则重新初始化地图
        this.initMapData();
      }
    },
    // 更新访问城市列表
    updateVisitedCities: function updateVisitedCities() {
      this.visitedCities = [];

      // 从足迹数据中更新访问城市列表
      for (var cityName in this.footprintData.cities) {
        var cityData = this.footprintData.cities[cityName];
        this.visitedCities.push({
          name: cityName,
          value: cityData.visitCount
        });
      }

      // 更新统计信息
      this.updateStats();
    },
    // 更新统计信息
    updateStats: function updateStats() {
      // 计算已访问城市数量
      var visitedCount = Object.keys(this.footprintData.cities).length;

      // 假设中国有34个省级行政区（包括特别行政区和台湾）
      var totalChinaRegions = 34;

      // 计算覆盖率
      var chinaRate = (visitedCount / totalChinaRegions * 100).toFixed(1);

      // 更新统计信息
      this.stats = {
        visitedCount: visitedCount,
        chinaRate: chinaRate + '%'
      };
    },
    // 获取已访问城市数据
    getVisitedCityData: function getVisitedCityData() {
      var mapType = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'china';
      // 简化处理，直接返回已访问城市数据
      if (mapType === 'world') {
        // 世界地图数据示例 - 简化为不带坐标的数据，避免复杂对象造成的问题
        return [{
          name: '中国',
          value: 1
        }];
      }

      // 返回中国地图数据
      return this.visitedCities;
    },
    // 获取城市坐标数据
    getCityCoordinates: function getCityCoordinates(mapType) {
      // 这里可以根据实际需要返回城市坐标数据
      // 简化示例，实际项目中可能需要更完整的坐标数据
      return {
        '北京': [116.4, 39.9],
        '上海': [121.4, 31.2],
        '广州': [113.2, 23.1],
        '中国': [116.4, 39.9]
      };
    }
  }
};
exports.default = _default;
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./node_modules/@dcloudio/uni-mp-weixin/dist/index.js */ 2)["default"], __webpack_require__(/*! ./node_modules/@dcloudio/uni-mp-weixin/dist/wx.js */ 1)["default"]))

/***/ }),

/***/ 129:
/*!***************************************************************************************************!*\
  !*** I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/footprint/footprint.vue?vue&type=style&index=0&lang=scss& ***!
  \***************************************************************************************************/
/*! no static exports found */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_8_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_sass_loader_dist_cjs_js_ref_8_oneOf_1_4_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/mini-css-extract-plugin/dist/loader.js??ref--8-oneOf-1-0!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/css-loader/dist/cjs.js??ref--8-oneOf-1-1!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/stylePostLoader.js!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--8-oneOf-1-2!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/postcss-loader/src??ref--8-oneOf-1-3!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/sass-loader/dist/cjs.js??ref--8-oneOf-1-4!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--8-oneOf-1-5!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!./footprint.vue?vue&type=style&index=0&lang=scss& */ 130);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_8_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_sass_loader_dist_cjs_js_ref_8_oneOf_1_4_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_8_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_sass_loader_dist_cjs_js_ref_8_oneOf_1_4_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0__);
/* harmony reexport (unknown) */ for(var __WEBPACK_IMPORT_KEY__ in _HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_8_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_sass_loader_dist_cjs_js_ref_8_oneOf_1_4_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0__) if(["default"].indexOf(__WEBPACK_IMPORT_KEY__) < 0) (function(key) { __webpack_require__.d(__webpack_exports__, key, function() { return _HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_8_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_sass_loader_dist_cjs_js_ref_8_oneOf_1_4_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0__[key]; }) }(__WEBPACK_IMPORT_KEY__));
 /* harmony default export */ __webpack_exports__["default"] = (_HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_8_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_sass_loader_dist_cjs_js_ref_8_oneOf_1_4_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_footprint_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0___default.a); 

/***/ }),

/***/ 130:
/*!*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/mini-css-extract-plugin/dist/loader.js??ref--8-oneOf-1-0!./node_modules/css-loader/dist/cjs.js??ref--8-oneOf-1-1!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--8-oneOf-1-2!./node_modules/postcss-loader/src??ref--8-oneOf-1-3!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/sass-loader/dist/cjs.js??ref--8-oneOf-1-4!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--8-oneOf-1-5!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/footprint/footprint.vue?vue&type=style&index=0&lang=scss& ***!
  \*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin
    if(false) { var cssReload; }
  

/***/ })

},[[118,"common/runtime","common/vendor"]]]);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/footprint/footprint.js.map