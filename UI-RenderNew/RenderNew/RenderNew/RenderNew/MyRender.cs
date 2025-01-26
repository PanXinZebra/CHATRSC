using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.Drawing;



namespace Render
{
    internal class MyRender
    {
        
        public  string m_savepath="K:\\sam\\renderresult\\";
        public  string m_imgpath => m_savepath + "main.jpg";
        
        public  string m_idpath => m_savepath + "id.text";
        public  string m_ctpath => m_savepath + "ct.text";

        public  string m_selectpath => m_savepath + "select.png";
        public string m_classificationpath => m_savepath + "class.png";

        public ZIDMap m_map=new ZIDMap();
        public ZPolygon m_polygon=new ZPolygon();
        public Image m_bmp;
        public Image m_selectbmp;
        public Image m_classificationbmp;


        public List<ZRemberPoint> points=new List<ZRemberPoint>();

        public int hss;
        public int lss;

        public int resize = 1;

        public bool havedata = false;

        public int focusid = -1;

        public void ReadFile()
        {
            var aa = Bitmap.FromFile(m_imgpath);
            m_bmp = new Bitmap(aa);  //防止Bitmap.FromFile加锁
            aa.Dispose();

            lss =m_bmp.Width;
            hss=m_bmp.Height;

            var aa1 = Bitmap.FromFile(m_selectpath);
            m_selectbmp= new Bitmap(aa1);  //防止Bitmap.FromFile加锁
            aa1.Dispose();

            var aa2 = Bitmap.FromFile(m_classificationpath);
            m_classificationbmp= new Bitmap(aa2);  //防止Bitmap.FromFile加锁
            aa2.Dispose();

            this.m_map.Obtain(m_idpath);
            this.m_polygon.Obtain(m_ctpath);
            havedata = true;
        }

        public void Draw(Graphics g)
        {
            if (this.havedata == false)
                return;
            DrawImg(g);

            if(focusid!=-1)
            {
                m_polygon.Draw(g,resize,focusid);
            }

        }

        public void DrawImg(Graphics g)
        {
            Rectangle rec1 = new Rectangle(0, 0, lss, hss);
            Rectangle rec2 = new Rectangle(0, 0, lss*resize, hss*resize);
            g.DrawImage(m_bmp, rec2, rec1, GraphicsUnit.Pixel);

            g.DrawImage(m_selectbmp, rec2, rec1, GraphicsUnit.Pixel);

            g.DrawImage(m_classificationbmp, rec2, rec1, GraphicsUnit.Pixel);

            
            foreach (var pt in points)
            {
                //画一个十字花的点
                Rectangle recx = new Rectangle(pt.x - 4, pt.y - 4, 8, 8);
                Rectangle recx2 = new Rectangle(pt.x - 5, pt.y - 5, 10, 10);
                Brush brush = new SolidBrush(Color.White);
                Pen pen = new Pen(new SolidBrush(Color.Blue));
                Pen pen2 = new Pen(new SolidBrush(Color.LightBlue));
                g.FillEllipse(brush, recx);
                g.DrawEllipse(pen, recx);
                g.DrawEllipse(pen2, recx2);
                Point pt1 = new Point(pt.x-3,pt.y-3);
                Point pt2 = new Point(pt.x+3,pt.y+3);
                Point pt3= new Point(pt.x+3,pt.y-3);
                Point pt4 = new Point(pt.x-3,pt.y+3);
                g.DrawLine(pen,pt1,pt2);
                g.DrawLine(pen, pt3, pt4);
            }

            

        }

        public void SaveImage()
        {
            Bitmap bmp = new Bitmap(lss * resize, hss * resize);
            Graphics gg = Graphics.FromImage(bmp);
            this.DrawImg(gg);
            bmp.Save(m_savepath+"a1.bmp");

        }

        public int GetID(int x , int y)
        {
            if (!havedata)
                return -1;
            int rx = x / resize;
            int ry = y / resize;

            if (rx < 0 || rx > lss)
                return -1;
            if (ry < 0 || ry > hss)
                return -1;

            return m_map.GetID(rx, ry);
        }


    }
}
