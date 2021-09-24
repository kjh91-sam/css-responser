# CSS pixel calculator for Responsive Design
## css-responser
> It helps you calculate pixel values for each breakpoint.  
> p.s. I made this because it's not fun to calculate every pixel value with ratio of each breakpoint.
- for desktop
    - Each pixel value is multiplied by the ratio of the breakpoint to its default size.
- for mobile
    - Converts all pixel values ​​to vw values ​​to their default size.
- How to use
    - Use this in your cli : `python css-responser.py file1 file2 ...`
    - Multiple files can be processed simultaneously. Just add the file names as many as you want.
- to see the test result, run this : `python css-responser.py testfile.liquid`

## convert-to-vw
> It helps you convert every pixel value to vw value based on default mobile size.  
> p.s. I need to use vw values ​​on mobile, but in Figma, only pixel values ​​can be checked, so I made this.
- It converts every pixel value in your stylesheet to vw value based on your default size setting.
- How to use
    - Use this in your cli : `python convert-to-vw.py file1 file2 ...`
    - Multiple files can be processed simultaneously. Just add the file names as many as you want.
- to see the test result, run this : `python convert-to-vw.py testfile.liquid`