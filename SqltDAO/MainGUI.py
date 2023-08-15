'''
Supporting namespace for generating Soft9000.com PyDAO projects.

Enjoy!

   -- Randall
'''

if __name__ == '__main__'
   from SqltDAO.CodeGen01.Meta import Meta
   from SqltDAO.main import Main as App
   print(f'Starting "{Meta.Title()}" ...')
   App.mainloop()
   print("Done!")
   quit()
