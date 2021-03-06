#!/usr/bin/env python
# Setup script for TVTK, numpy.distutils based.
#
#
import os, sys


def configuration(parent_package=None, top_path=None):
    from os.path import join
    from numpy.distutils.misc_util import Configuration
    config = Configuration('tvtk',parent_package,top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)


    config.add_subpackage('custom')
    config.add_subpackage('pipeline')
    config.add_data_dir('pipeline/images')
    config.add_data_dir('pyface/images')
    config.add_data_dir('tools/images')

    config.add_subpackage('plugins')
    config.add_subpackage('plugins.*')

    config.add_subpackage('tools')
    config.add_subpackage('util')

    config.add_subpackage('tests')

    # Numpy support.
    config.add_extension('array_ext',
                         sources = [join('src','array_ext.c')],
                         depends = [join('src','array_ext.pyx')],
                         )

    tvtk_classes_zip_depends = config.paths(
        'code_gen.py','wrapper_gen.py', 'special_gen.py',
        'tvtk_base.py', 'indenter.py', 'vtk_parser.py')

    return config


def gen_tvtk_classes_zip():
    from code_gen import TVTKGenerator
    target = os.path.join(os.path.dirname(__file__), 'tvtk_classes.zip')
    output_dir = os.path.dirname(target)
    try:
        os.mkdir(output_dir)
    except:
        pass
    print '-'*70
    if os.path.exists(target):
        print 'Deleting possibly old TVTK classes'
        os.unlink(target)
    print "Building TVTK classes...",
    sys.stdout.flush()
    cwd = os.getcwd()
    os.chdir(output_dir)
    gen = TVTKGenerator('')
    gen.generate_code()
    gen.build_zip(True)
    os.chdir(cwd)
    print "Done."
    print '-'*70


def vtk_version_changed(zipfile):
    """Checks the ZIP file's VTK build version versus the current
    installed version of VTK and returns `True` if the versions are
    different.

    """
    result = True
    if os.path.exists(zipfile):
        import vtk
        vtk_version = vtk.vtkVersion().GetVTKVersion()[:3]
        sys.path.append(zipfile)
        try:
            from tvtk_classes.vtk_version import vtk_build_version
        except ImportError:
            result = True
        else:
            if vtk_version != vtk_build_version:
                result = True
            else:
                result = False
        sys.path.pop()

    return result

