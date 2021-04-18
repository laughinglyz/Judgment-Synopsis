<template>
    <div>
        <breadcrumb :paths="paths"></breadcrumb>
        <div>
            <v-row>
            <v-col class="col-12" style="background: white">
                <h2 class="ml-2" v-html="title"></h2>
                <div class="d-flex flex-wrap justify-space-between metadata">
                    <div class="ml-2">{{date}}</div>
                    <div class="ml-2">{{neutral}}</div>
                    <div class="ml-2" v-if="acts">{{acts}}</div>
                    <div class="ml-2" v-if="hkc">{{hkc}}</div>
                    <div class="ml-2" v-if="hklrd">{{hklrd}}</div>
                    <div class="ml-2" v-if="hkcfar">{{hkcfar}}</div>
                </div>
                <v-divider></v-divider>
                <div class="d-flex flex-wrap justify-space-between metadata">
                    <v-btn text color="primary" class="ml-2" v-if="acts" :href="lawcite_path">LawCite</v-btn>
                    <v-btn text color="primary" class="ml-2" @click="trigger_noteup"> Noteup</v-btn>
                    <v-btn text color="primary" class="ml-2" v-if="trans" :to="trans_path"> {{lang}}</v-btn>
                    <v-btn text color="primary" class="mx-2" v-if="doc" :href="doc">MS Word Format</v-btn>
                    <v-dialog v-if="appealhistory" v-model="dialog">
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn
                            color="primary"
                            text
                            v-bind="attrs"
                            v-on="on"
                          >
                            Appeal History
                          </v-btn>
                        </template>
                    <v-card>
                    <v-card-title>
                        <span class="headline">{{title}} Appeal History</span>
                    </v-card-title>
                    <v-card-text v-html="appealhistory"></v-card-text>
                    </v-card>
                    </v-dialog>
                    <v-btn text color="primary" class="ml-2" @click="toggle_highlight">Highlight Keyinfo</v-btn>
                </div>
                <div class="case-content" v-for="corr in corrs" v-bind:key="corr.id">
                    <div v-html="corr.content"></div>
                </div>
                <div v-if="content" class="case-content" v-html="content"></div>
                <div v-else class="case-content">Currently, only Word format is available.</div>
            </v-col>
            </v-row>
        </div>
        <v-overlay :value="overlay">
        <v-progress-circular
          indeterminate
          size="64"
        ></v-progress-circular>
      </v-overlay>
    </div>
</template>



<script>
    import Breadcrumb from '../components/applayout/Breadcrumb'
    import search from '../search'
    export default {
        name:'Case',
        components:{
            Breadcrumb
        },
        data(){
            return {
                dialog:false,
                overlay:false,
                db_name:'',
                id:'',
                title:'',
                neutral:'',
                hkc:"",
                hklrd:"",
                hkcfar:"",
                acts:'',
                date:'',
                content:'',
                doc:'',
                corrs:[],
                path:'',
                trans:false,
                appeals:[],
                lang:'',
                trans_path:'',
                lawcite_path:'',
                appealhistory:'',
                highlight:false,
            }
        },
        methods:{
        trigger_noteup(){
                 this.$router.push({name:'search-results', query:{noteup:this.$route.path}})
        },
        toggle_highlight(){
            this.highlight = !this.highlight;
            var important_sents = document.getElementsByClassName('important');
            for (var i = 0; i < important_sents.length; i++) {
                if (this.highlight){
                    important_sents[i].style.color = "red";}
                else{
                    important_sents[i].style.color = "black";}
            }
        },
        get_case(){
          this.overlay=true
         search.get_nonlegisfile(this.$route.path).then(res =>{
             if (res["hits"]["total"]['value']>0){
             const file = res["hits"]["hits"][0]['_source']
             this.title = file['title']
             this.id=file['id']
           this.date = file['date'].slice(0, 10)
                 if (this.date =='1900-01-01'){
                     this.date = 'UNKNOWN'
                 }
           this.acts = file['acts']
           this.neutral = file['neutral']
           this.hkc = file['hkc']
           this.hklrd = file['hklrd']
           this.hkcfar = file['hkcfar']
           this.trans = file['is_translated']
           if(this.trans){
                if(this.$route.params['lang'] == 'en'){
                    this.lang = 'Chinese'
                    this.trans_path = this.$route.path.replace('en', 'tc')
                }else{
                    this.lang = 'English'
                    this.trans_path = this.$route.path.replace('tc', 'en')
                }
           }
           if('appealhistory' in file){
               this.appealhistory = file['appealhistory']
           }
           this.doc = file['doc']
           this.content = file['content']
           this.db_name = file['db_name']
           this.path = file['path']
           if (this.path.includes('/cases/')){
               if (this.path.includes('/ukpc/')==false){
               this.get_corrs()
               }
          }
            this.overlay=false
          }})
        },
        get_corrs(){
            this.overlay=true
         search.get_corrs(this.id).then(res =>{
             this.corrs = res['hits']['hits'].map(function(i){
                        return i['_source'];
                    })
             this.overlay=false
         })
        },
        },
        computed:{
            paths(){
                if (this.path){
              return  [{text: 'HKLII', disabled: false, href: '/'},
            {text: this.$i18n.t('message.dbs'), disabled: false, href: '/databases'},
            {text: this.db_name, disabled: false, href: this.path.split('/').splice(0,4).join('/')+'/'},
            {text: this.neutral, disabled: true, href: this.path}
            ]
            }
                 return []
        }
        },
        watch:{
            '$route.path': function () {
            this.get_case()
            const params = this.$route.params
            this.lawcite_path = "http://www.austlii.edu.au/cgi-bin/LawCite?cit="+params.year+" "+ params.abbr+" "+params.num
            }
        },
        mounted(){
            this.get_case()
            const params = this.$route.params
            this.lawcite_path = "http://www.austlii.edu.au/cgi-bin/LawCite?cit="+params.year+" "+ params.abbr+" "+params.num
        }
    }
</script>
<style>
    .case-content{
        width:95%;
        margin:10px auto;
    }
    .appeal{
        max-width:90%;
        margin:0 auto;
    }
</style>