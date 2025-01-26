using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Drawing;

namespace Render
{
    internal class ZPolygon
    {
        public List<ZAPoly> plylist=new List<ZAPoly>();
        public Dictionary<int,ZAPoly> indexs=new Dictionary<int,ZAPoly>();



        public void Obtain(String FileName)
        {
            plylist.Clear();
            indexs.Clear();
            try
            {
                String[] lines = File.ReadAllLines(FileName);


                foreach(String line in lines)
                {
                    ZAPoly a = new ZAPoly();
                    a.Obtain(line);
                    plylist.Add(a);
                }

                foreach(ZAPoly a in plylist)
                {
                    indexs[a.ID] = a;
                }
                

            }
            catch
            {

            }
        }

       

        public void Draw(Graphics g, int resize, int focusid)
        {
            var focuselist = indexs[focusid];

            if (focuselist == null)
                return;

            var a = focuselist;

            if (focusid != 86)
                focusid = focusid;
            a.DrawMe(g, resize);
          
            /*
            foreach (ZAPoly a in plylist)
            {
                a.DrawMe(g, resize);
            }*/

        }


    }
}
