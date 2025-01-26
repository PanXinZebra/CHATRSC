using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
namespace Render
{
    internal class ZIDMap
    {
        public int hss;
        public int lss;
        public int[][] map;


        public int GetID(int rx, int ry)
        {
            return map[ry][rx];
        }

        public void Obtain(String FileName)
        {
            try
            {
                String[] lines = File.ReadAllLines(FileName);


                String[] mysize = lines[0].Split(new char[] { ' ', '[', ']', '\n',',' }, StringSplitOptions.RemoveEmptyEntries);
                this.hss =int.Parse( mysize[0]);
                this.lss = int.Parse(mysize[1]);

                map = new int[this.hss][];
                for (int i = 0; i < this.hss; i++)
                {
                    map[i] = new int[this.lss];
                    var xx = lines[i+1].Split(new char[] { ' ', '[', ']', '\n', ',' }, StringSplitOptions.RemoveEmptyEntries);
                    for (int j = 0; j < this.lss; j++)
                    {
                        map[i][j] = int.Parse(xx[j]);
                    }
                }
                
            }
            catch
            {

            }


        }
    }
}
