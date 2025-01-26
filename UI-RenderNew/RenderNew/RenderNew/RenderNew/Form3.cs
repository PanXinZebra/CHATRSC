﻿using CefSharp;
using Render;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using RestSharp;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json;
using NetMQ;
using NetMQ.Sockets;

namespace RenderNew
{
    public partial class Form3 : Form
    {
        private String left_id = "result_";

        private long id_ = 0;

        MyRender render = new MyRender();

        bool startinputpoint = false;
        public Form3()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            ReadAll();
        }
        private void ReadAll()
        {
            render.ReadFile();

            pictureBox1.Size = new Size(render.lss, render.hss);
            pictureBox1.Invalidate();
        }

        private void button4_Click(object sender, EventArgs e)
        {
            render.points = new List<ZRemberPoint>();
            startinputpoint = true;
        }

        private void button5_Click(object sender, EventArgs e)
        {
            render.points = new List<ZRemberPoint>();
            startinputpoint = false;
        }

        private void button7_Click(object sender, EventArgs e)
        {
            String s = "[";
            bool first = true;
            foreach (var pt in render.points)
            {
                if (first)
                {
                    first = false;
                }
                else
                {
                    s += ", ";
                }
                s += pt.segid.ToString();

            }
            s += "]";
            textBox3.Text = s;

            s = "[";
            first = true;

            foreach (var pt in render.points)
            {
                if (first)
                {
                    first = false;
                }
                else
                {
                    s += ", ";
                }
                s += "[" + pt.x.ToString() + "," + pt.y.ToString() + "]";

            }
            s += "]";
            textBox4.Text = s;
        }

        private void button6_Click(object sender, EventArgs e)
        {
            render.SaveImage();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            render.focusid = 18;
            pictureBox1.Invalidate();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            pictureBox1.Invalidate();
        }

        private void pictureBox1_MouseClick(object sender, MouseEventArgs e)
        {
            if (!(startinputpoint))
                return;
            int id = render.GetID(e.X, e.Y);

            textBox2.Text = id.ToString();

            render.focusid = id;

            textBox1.Text = e.X + ",  " + e.Y;



            ZRemberPoint point = new ZRemberPoint();
            point.segid = id;
            point.x = e.X;
            point.y = e.Y;
            render.points.Add(point);
            pictureBox1.Invalidate();
        }

        private void pictureBox1_MouseMove(object sender, MouseEventArgs e)
        {
            int id = render.GetID(e.X, e.Y);
            textBox2.Text = id.ToString();

            render.focusid = id;

            textBox1.Text = e.X + ",  " + e.Y;
            pictureBox1.Invalidate();
        }

        private void pictureBox1_Paint(object sender, PaintEventArgs e)
        {
            render.Draw(e.Graphics);
        }

        private void button8_Click(object sender, EventArgs e)
        {
         
            this.button8.Enabled = false;
            String content = this.textBox5.Text.ToString();
            if (content==null|| content.Equals("")) {
                MessageBox.Show("请输入信息");
                return;
            }





            String s = "[";
            bool first = true;
            foreach (var pt in render.points)
            {
                if (first)
                {
                    first = false;
                }
                else
                {
                    s += ", ";
                }
                s += pt.segid.ToString();

            }
            s += "]";

            String segmentstring = "The segments parameter is " + s;


            String sendtxt = "";
            if (content.EndsWith("."))
                sendtxt=content + " " + segmentstring;
            else
                sendtxt = content + ". " + segmentstring;

            /*

            RestClient client;
            client = new RestClient("http://localhost:8888/process_content/?content="+ content);
            RestRequest req = new RestRequest("", Method.Get);
            
            RestResponse res = client.Execute(req);
            

            if (res.IsSuccessful)
            {
                //MessageBox.Show(res.Content);
                JObject jo = JsonConvert.DeserializeObject<JObject>(res.Content);

                if (jo["status"].ToString().Equals("success")) {
                    //MessageBox.Show(jo["processed_result"].ToString());
                    createRight(this.textBox5.Text.ToString());
                    createLeft(jo["processed_result"].ToString());
                    chromiumWebBrowser1.ExecuteScriptAsync("document.getElementById('result_n').scrollIntoView();");
                }
                else
                {
                    MessageBox.Show("获取数据失败");
                }

              

            }
            else
            {
                MessageBox.Show("获取数据失败");
            }*/

            using (var requester = new RequestSocket())
            {
                
                requester.Connect("tcp://localhost:5557");
                string request = sendtxt;
                // 发送请求消息
                requester.SendFrame(request);
                Console.WriteLine($"Sent request: {request}");
                // 接收响应消息
                string response = requester.ReceiveFrameString();
                Console.WriteLine($"Received response: {response}");
                
                //var response = "Loading complete. You can try to control the classification results through conversation.";
                createRight(sendtxt.Replace("'", ""));
                createLeft(response.ToString());
                chromiumWebBrowser1.ExecuteScriptAsync("document.getElementById('result_n').scrollIntoView();");
            }




            this.textBox5.Text = "";
            this.button8.Enabled = true;

            ReadAll();
        }

        private void createRight(string content)
        {


            string rightHtml = @"
                var elem = document.getElementById('result_0');
               var newContent = '<div class=""chat_content_group self""  id=""{{id}}""><img class=""chat_content_avatar"" src=""data:image/jpg;base64,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"" width=""40px"" height=""40px""><p class=""chat_nick"">User</p><p class=""chat_content"">{{content}}</p></div>';
                elem.insertAdjacentHTML('beforeend', newContent);"
      ;

            rightHtml = rightHtml.Replace("{{content}}", content);

        
            id_ = id_ + 1;
            rightHtml = rightHtml.Replace("{{id}}", left_id + id_.ToString());

            //chromiumWebBrowser1.ExecuteScriptAsync(rightHtml);
            chromiumWebBrowser1.EvaluateScriptAsPromiseAsync(rightHtml).Wait();
            Console.WriteLine(":" + left_id + id_.ToString());
        }



        private void createLeft(string content)
        {


            string leftHtml = @"
                var elem = document.getElementById('result_0');
                var newContent = '<div class=""chat_content_group buddy""  id=""{{id}}""> <img class=""chat_content_avatar"" src=""data:image/jpg;base64,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"" width=""40px"" height=""40px""> <p class=""chat_nick"">Chat-RSC</p>  <p class=""chat_content"">{{content}}</p>  </div>';
                elem.insertAdjacentHTML('beforeend', newContent);";


            leftHtml = leftHtml.Replace("{{content}}", content);
        
            id_ = id_ + 1;
            leftHtml = leftHtml.Replace("{{id}}", left_id + id_.ToString());

            //chromiumWebBrowser1.ExecuteScriptAsync(leftHtml);
            chromiumWebBrowser1.EvaluateScriptAsPromiseAsync(leftHtml).Wait();
            Console.WriteLine(":" + left_id + id_.ToString());
        }


        private void initHTML()
        {
            String html1 = @"<html><head> <meta charset=""UTF-8"">
<script type=""text/javascript"">window.location.hash = ""#ok"";</script>
<style type=""text/css"">

/*滚动条宽度*/  
::-webkit-scrollbar {  
    width: 8px;  
}  
   
/* 轨道样式 */  
::-webkit-scrollbar-track {  
  
}  
   
/* Handle样式 */  
::-webkit-scrollbar-thumb {  
    border-radius: 10px;  
    background: rgba(0,0,0,0.2);   
}  
  
/*当前窗口未激活的情况下*/  
::-webkit-scrollbar-thumb:window-inactive {  
    background: rgba(0,0,0,0.1);   
}  
  
/*hover到滚动条上*/  
::-webkit-scrollbar-thumb:vertical:hover{  
    background-color: rgba(0,0,0,0.3);  
}  
/*滚动条按下*/  
::-webkit-scrollbar-thumb:vertical:active{  
    background-color: rgba(0,0,0,0.7);  
}  
  
textarea{width: 500px;height: 300px;border: none;padding: 5px;}  

    .chat_content_group.self {
text-align: right;
}
.chat_content_group {
padding: 10px;
}
.chat_content_group.self>.chat_content {
text-align: left;
}
.chat_content_group.self>.chat_content {
background: #7ccb6b;
color:#fff;
/*background: -webkit-gradient(linear,left top,left bottom,from(white,#e1e1e1));
background: -webkit-linear-gradient(white,#e1e1e1);
background: -moz-linear-gradient(white,#e1e1e1);
background: -ms-linear-gradient(white,#e1e1e1);
background: -o-linear-gradient(white,#e1e1e1);
background: linear-gradient(#fff,#e1e1e1);*/
}
.chat_content {
display: inline-block;
min-height: 16px;
max-width: 50%;
color:#292929;
background: #f0f4f6;
/*background: -webkit-gradient(linear,left top,left bottom,from(#cf9),to(#9c3));
background: -webkit-linear-gradient(#cf9,#9c3);
background: -moz-linear-gradient(#cf9,#9c3);
background: -ms-linear-gradient(#cf9,#9c3);
background: -o-linear-gradient(#cf9,#9c3);
background: linear-gradient(#cf9,#9c3);*/
-webkit-border-radius: 5px;
-moz-border-radius: 5px;
border-radius: 5px;
padding: 10px 15px;
word-break: break-all;
/*box-shadow: 1px 1px 5px #000;*/
line-height: 1.4;
}

.chat_content_group.self>.chat_nick {
text-align: right;
}
.chat_nick {
font-size: 14px;
margin: 0 0 10px;
color:#8b8b8b;
}

.chat_content_group.self>.chat_content_avatar {
float: right;
margin: 0 0 0 10px;
}

.chat_content_group.buddy {
text-align: left;
}
.chat_content_group {
padding: 10px;
}
.chat_content_avatar {
float: left;
width: 40px;
height: 40px;
margin-right: 10px;
}
.imgtest{margin:10px 5px;
overflow:hidden;}
.list_ul figcaption p{
font-size:12px;
color:#aaa;
}
.imgtest figure div{
display:inline-block;
margin:5px auto;
width:100px;
height:100px;
border-radius:100px;
border:2px solid #fff;
overflow:hidden;
-webkit-box-shadow:0 0 3px #ccc;
box-shadow:0 0 3px #ccc;
}
.imgtest img{width:100%;
min-height:100%; text-align:center;}
    </style>
</head><body>  
<div id=""result_0"">

</div>

<div id=""result_n"">

</div>
";
            chromiumWebBrowser1.LoadHtml(html1);
        }

        private void Form3_Load(object sender, EventArgs e)
        {
            initHTML();
            String html = @"
<div class=""chat_content_group self"">
    
    <img class=""chat_content_avatar"" src=""data:image/jpg;base64,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"" width=""40px"" height=""40px"">
    
        <p class=""chat_nick"">阿狸萌萌哒</p>
    
    
    <p class=""chat_content"">测试一下QQ聊天气泡</p>
</div>
<div class=""chat_content_group buddy"" id=""anchorPoint"">

        <img class=""chat_content_avatar"" src=""data:image/jpg;base64,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"" width=""40px"" height=""40px"">

        <p class=""chat_nick"">兔纸</p>


        <p class=""chat_content""><img class=""EQQ_faceImg"" src="""" width=""24px"" height=""24px"">怎么实现的呢</p>
    </div>
";
        }

        private void label3_Click(object sender, EventArgs e)
        {

        }
    }
}
