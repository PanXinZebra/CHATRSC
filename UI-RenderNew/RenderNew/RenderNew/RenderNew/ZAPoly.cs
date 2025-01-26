using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Render
{
    internal class ZAPoly
    {
        public int ID;
        public List<Point> list = new List<Point>();


        public Rectangle myrect;

        public Bitmap mybitmap;

        public void SetRect()
        {
            int xmax = 0;
            int xmin = 99999999;
            int ymin = 99999999;
            int ymax = 0;

         
            foreach (var pt in list)
            {
                if (xmax < pt.X)
                    xmax = pt.X;
                if (xmin > pt.X)
                    xmin = pt.X;
                if (ymax < pt.Y)
                    ymax = pt.Y;
                if (ymin > pt.Y)
                    ymin = pt.Y;
            }
            
            myrect = new Rectangle(xmin, ymin, xmax - xmin+1, ymax - ymin+1);

        }
        public void SetBitmap()
        {
            // 创建一个与点列表大小相同的 Bitmap 对象
            mybitmap = new Bitmap(myrect.Width, myrect.Height);

            Color color = Color.FromArgb(180,0,200,255);
            // 遍历点列表，并使用 SetPixel 方法将每个点的颜色设置到 Bitmap 对象中
            foreach (Point point in list)
            {
                mybitmap.SetPixel(point.X-myrect.Left, point.Y-myrect.Top, color);
            }

            //mybitmap.Save("K:\\sam\\aa\\"+ID+".bmp");
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="value"></param>
        public void Obtain(String value)
        {
            list.Clear();
            String[] values = value.Split(new char[] { ' ', '[', ']', '\n',','}, StringSplitOptions.RemoveEmptyEntries);
            ID=int.Parse(values[0]);
            for(int i = 1; i < values.Length; i=i+2)
            {
                var x = int.Parse(values[i]);
                var y = int.Parse(values[i+1]);
                Point pt=new Point(x,y);
                list.Add(pt);
            }
            this.SetRect();
            this.SetBitmap();
        }

        public void DrawMe(Graphics g, int resize)
        {
            


            Rectangle rec1 = new Rectangle(0, 0, myrect.Width, myrect.Height);
            Rectangle rec2 = new Rectangle(myrect.Left*resize, myrect.Top*resize, myrect.Width*resize, myrect.Height*resize);
            g.DrawImage(this.mybitmap, rec2, rec1, GraphicsUnit.Pixel);
        }

        
    }
}
